import string
from collections.abc import Callable


def main(filename: str):
    with open(filename) as f:
        instruction_strings = [_.strip("\n") for _ in f.readlines()]
        instructions = build_instruction_set(instruction_strings)

    machine = [0, 0, 0, 0]
    instruction_pointer = 0
    while instruction_pointer < len(instructions):
        instruction_pointer += instructions[instruction_pointer](machine)
    print(f"When the first machine halts, register a = {machine[0]}")

    machine = [0, 0, 1, 0]
    instruction_pointer = 0
    while instruction_pointer < len(instructions):
        instruction_pointer += instructions[instruction_pointer](machine)
    print(f"When the second machine halts, register a = {machine[0]}")


def build_instruction_set(instructions: list[str]) -> list[Callable]:
    instruction_set = []
    for instruction in instructions:
        func, *args = instruction.split(" ")
        match func:
            case "cpy":
                instruction_set.append(build_copy_function(*args))
            case "inc":
                instruction_set.append(build_increase_function(*args))
            case "dec":
                instruction_set.append(build_decrease_function(*args))
            case "jnz":
                instruction_set.append(build_jump_function(*args))
    return instruction_set


def get_index_for_target(target: str) -> int:
    return ord(target) - ord("a")


def build_copy_function(source: str, target: str) -> Callable:
    tgt_idx = get_index_for_target(target)
    try:
        delta = int(source)

        def copy(machine):
            machine[tgt_idx] = delta
            return 1

        return copy
    except ValueError:
        src_idx = get_index_for_target(source)

        def copy(machine):
            machine[tgt_idx] = machine[src_idx]
            return 1

        return copy


def build_increase_function(target: str) -> Callable:
    idx = get_index_for_target(target)
    def increase(machine: list[int]):
        machine[idx] += 1

        return 1

    return increase


def build_decrease_function(target: str) -> Callable:
    idx = get_index_for_target(target)
    def decrease(machine: list[int]):
        machine[idx] -= 1

        return 1

    return decrease


def build_jump_function(test_register: str, offset_string: str) ->  Callable:
    offset = int(offset_string)
    if test_register in string.ascii_lowercase:
        idx = get_index_for_target(test_register)
        def jump(machine: list[int]):
            if machine[idx] != 0:
                return offset
            return 1
        return jump

    test_constant = int(test_register)
    if test_constant != 0:
        def jump(_: list[int]):
            return offset

        return jump

    def jump(_: list[int]):
        return 1

    return jump


if __name__ == "__main__":
    main("input.txt")
