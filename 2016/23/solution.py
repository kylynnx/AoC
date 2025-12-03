import string
from collections.abc import Callable

def noop(**_):
    return 1


def faculty(value: int) -> int:
    if value == 1:
        return 1

    return value * faculty(value - 1)


def main(filename: str):
    with open(filename) as f:
        instructions = [_.strip("\n") for _ in f.readlines()]

    initial_value = 7
    machine = [initial_value, 0, 0, 0]
    instruction_pointer = 0
    while instruction_pointer < len(instructions):
        func = build_instruction(instructions[instruction_pointer])
        instruction_pointer += func(machine=machine, instructions=instructions, pointer=instruction_pointer)

    result = machine[0]
    print(f"When the first machine halts, register a = {result}")

    # Figured out that after a certain point this machine calculates the faculty of the input and adds a constant.
    # Couldn't be bothered to programmatically analysing the instructions and introducing a `mul` instruction.
    offset = result - faculty(initial_value)
    second = faculty(12) + offset
    print(f"When the second machine halts, register a = {second}")


def build_instruction(instruction: str) -> Callable:
    func, *args = instruction.split(" ")
    match func:
        case "cpy":
            return build_copy_function(*args)
        case "inc":
            return build_increase_function(*args)
        case "dec":
            return build_decrease_function(*args)
        case "jnz":
            return build_jump_function(*args)
        case _:
            return build_toggle_function(*args)


def get_index_for_target(target: str) -> int:
    return ord(target) - ord("a")


def build_copy_function(source: str, target: str) -> Callable:
    try:
        tgt_idx = get_index_for_target(target)
    except ValueError:
        return noop

    try:
        delta = int(source)

        def copy(machine, **_):
            machine[tgt_idx] = delta
            return 1

        return copy
    except ValueError:
        src_idx = get_index_for_target(source)

        def copy(machine, **_):
            machine[tgt_idx] = machine[src_idx]
            return 1

        return copy


def build_increase_function(target: str) -> Callable:
    idx = get_index_for_target(target)
    def increase(machine: list[int], **_):
        machine[idx] += 1

        return 1

    return increase


def build_decrease_function(target: str) -> Callable:
    idx = get_index_for_target(target)
    def decrease(machine: list[int], **_):
        machine[idx] -= 1

        return 1

    return decrease


def build_jump_function(test_register: str, offset_string: str) ->  Callable:
    if test_register in string.ascii_lowercase:
        idx = get_index_for_target(test_register)

        if offset_string in string.ascii_lowercase:
            offset_idx = get_index_for_target(offset_string)
            def jump(machine: list[int], **_):
                if machine[idx] != 0:
                    return machine[offset_idx]
                return 1
        else:
            def jump(machine: list[int], **_):
                if machine[idx] != 0:
                    return int(offset_string)

                return 1

        return jump

    test_constant = int(test_register)
    if test_constant != 0:
        if offset_string in string.ascii_lowercase:
            offset_idx = get_index_for_target(offset_string)
            def jump(machine, **_):
                return machine[offset_idx]
        else:
            def jump(**_):
                return int(offset_string)

        return jump

    return noop


def build_toggle_function(test_register: str) -> Callable:
    idx = get_index_for_target(test_register)

    def toggle(machine: list[int], instructions: list[str], pointer: int):
        tgl_index = pointer + machine[idx]

        if tgl_index >=  len(instructions):
            return 1

        instruction = instructions[tgl_index]
        new_instruction = ""
        previous, *args = instruction.split(" ")

        match previous:
            case "cpy":
                new_instruction = "jnz"
            case "inc":
                new_instruction = "dec"
            case "dec":
                new_instruction = "inc"
            case "jnz":
                new_instruction = "cpy"
            case "tgl":
                new_instruction = "inc"

        instructions[tgl_index] = " ".join([new_instruction] + args)

        return 1

    return toggle


if __name__ == "__main__":
    main("input.txt")
