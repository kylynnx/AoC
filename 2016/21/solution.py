import re
from itertools import permutations


def main(clear_password: str, initial_scrambled_password: str, operations_file: str):
    with open(operations_file) as f:
        operations = [_.strip("\n") for _ in f.readlines()]

    scrambled_password=scramble_password(unscrambled_password=clear_password, operations=operations)
    print(f"The scrambled passcode is {scrambled_password}.")

    unscrambled_password="PASSWORD COULD NOT BE FOUND"
    for permutation in permutations(scrambled_password):
        if scramble_password("".join(permutation), operations) == initial_scrambled_password:
            unscrambled_password="".join(permutation)

    print(f"The unscrambled passcodes are {unscrambled_password}.")


def scramble_password(unscrambled_password: str, operations: list[str]) -> str:
    scrambled_password = unscrambled_password
    for operation in operations:
        scrambled_password = execute_operation(target=scrambled_password, operation=operation)
    return scrambled_password


def execute_operation(target: str, operation: str) -> str:
    if operation.startswith("swap position"):
        return swap_positions(target=target, operation=operation)

    elif operation.startswith("swap letter"):
        return swap_letters(target=target, operation=operation)

    elif operation.startswith("reverse"):
        return reverse_positions(target=target, operation=operation)

    elif operation.startswith("move"):
        return move_positions(target=target, operation=operation)

    elif operation.startswith("rotate based"):
        return rotate_based_on_letter(target=target, operation=operation)

    return rotate_by_offset(target=target, operation=operation)


def swap_positions(target: str, operation: str) -> str:
    match = re.match(r"swap position (\d+) with position (\d+)", operation)
    x = int(match.group(1))
    y = int(match.group(2))

    if x == y:
        return target
    elif x > y:
        return _swap(target=target, front=y, back=x)

    return _swap(target=target, front=x, back=y)


def _swap(target: str, front: int, back: int) -> str:
    return target[:front] + target[back] + target[front+1:back] + target[front] + target[back+1:]


def swap_letters(target: str, operation: str) -> str:
    re_match = re.match(r"swap letter ([a-z]) with letter ([a-z])", operation)
    first_letter = re_match.group(1)
    idx_first_letter = target.index(first_letter)
    second_letter = re_match.group(2)
    idx_second_letter = target.index(second_letter)

    if idx_first_letter == idx_second_letter:
        return target

    target = _set_letter(target=target, idx=idx_first_letter, letter=second_letter)
    target = _set_letter(target=target, idx=idx_second_letter, letter=first_letter)

    return target


def _set_letter(target: str, idx: int, letter: str):
    return target[:idx] + letter + target[idx+1:]


def reverse_positions(target: str, operation: str) -> str:
    re_match = re.match(r"reverse positions (\d+) through (\d+)", operation)

    x = int(re_match.group(1))
    y = int(re_match.group(2))

    if x == y:
        return target

    return target[:x] + target[x:y + 1][::-1] + target[y + 1:]


def move_positions(target: str, operation: str) -> str:
    re_match = re.match(r"move position (\d+) to position (\d+)", operation)

    from_position = int(re_match.group(1))
    to_position = int(re_match.group(2))

    from_letter = target[from_position]

    if from_position == to_position:
        return target

    if from_position > to_position:
        return target[:to_position] + from_letter + target[to_position:from_position] + target[from_position + 1:]

    return target[:from_position] + target[from_position + 1:to_position + 1] + from_letter + target[to_position + 1:]


def rotate_based_on_letter(target: str, operation: str) -> str:
    re_match = re.match(r"rotate based on position of letter ([a-z])", operation)
    steps = target.index(re_match.group(1))

    if steps >= 4:
        steps += 1
    steps += 1
    steps = len(target) - steps

    if steps < 0:
        steps += len(target)

    if steps == 0:
        return target

    return _rotate(target=target, steps=steps)


def rotate_by_offset(target: str, operation: str) -> str:
    re_match = re.match(r"rotate (left|right) (\d+) steps?", operation)
    steps = int(re_match.group(2))

    if steps == 0:
        return target

    rotate_left = re_match.group(1) == "left"

    if rotate_left:
        return _rotate(target=target, steps=steps)

    return _rotate(target=target, steps=len(target) - steps)


def _rotate(target: str, steps: int) -> str:
    return target[steps:] + target[:steps]


if __name__ == "__main__":
    main(clear_password="abcde", initial_scrambled_password="decab", operations_file="test.txt")
    main(clear_password="abcdefgh", initial_scrambled_password="fbgdceah", operations_file="input.txt")
