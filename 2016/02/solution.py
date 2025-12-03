from collections.abc import Callable
from enum import Enum

key_lookup_rectangular = {
    0: "7",
    1: "8",
    2: "9",
    1j: "4",
    1 + 1j: "5",
    2 + 1j: "6",
    2j: "1",
    1 + 2j: "1",
    2 + 2j: "3",
}

key_lookup_diamond = {
    2j: "1",
    -1 + 1j: "2",
    1j: "3",
    1 + 1j: "4",
    -2: "5",
    -1: "6",
    0: "7",
    1: "8",
    2: "9",
    -1 - 1j: "A",
    -1j: "B",
    1 - 1j: "C",
    -2j: "D",
}


class Instruction(Enum):
    U = 1j
    L = -1
    R = 1
    D = -1j


def load_instructions(filename: str) -> list:
    with open(filename) as f:
        return [_.strip("\n") for _ in f.readlines()]


def remove_excess_instructions(instruction: str, max_count: int = 2) -> str:
    shortened_instruction = ""
    last_step = ""
    step_count = 1
    for step in instruction:
        if last_step != step:
            shortened_instruction += step
            last_step = step
            step_count = 1
        elif step_count < max_count:
            shortened_instruction += step
            step_count += 1
        else:
            continue
    return shortened_instruction


def clean_instructions(instructions: list, max_count: int = 2) -> list:
    return [remove_excess_instructions(_, max_count=max_count) for _ in instructions]


def gauge_position_rectangular(position: complex, delta: complex) -> complex:
    new_position = position + delta
    return min(max(new_position.real, 0), 2) + min(max(new_position.imag, 0), 2) * 1j


def gauge_position_diamond(position: complex, delta: complex) -> complex:
    new_position = position + delta

    if abs(new_position.real) + abs(new_position.imag) > 2:
        return position

    return new_position


def follow_instructions(
        instructions: list, key_lookup: dict[complex, str], starting_point: complex = 1 + 1j,
        gauge: Callable[[complex, complex], complex] = gauge_position_rectangular) -> str:
    current_point = starting_point
    result = ""
    for instruction in instructions:
        current_point = follow_instruction(current_point, instruction=instruction, gauge=gauge)
        result += key_lookup[current_point]

    return result


def follow_instruction(starting_point: complex, instruction: str,
                       gauge: Callable[[complex, complex], complex]) -> complex:
    for step in instruction:
        starting_point = gauge(starting_point, Instruction[step].value)
    return starting_point


def main(filename: str):
    instructions = load_instructions(filename)

    cleaned_instructions = clean_instructions(instructions)
    result = follow_instructions(
        instructions=cleaned_instructions, key_lookup=key_lookup_rectangular, starting_point=1 + 1j
    )
    print(result)

    cleaned_instructions = clean_instructions(instructions, max_count=4)
    result = follow_instructions(
        instructions=cleaned_instructions,
        key_lookup=key_lookup_diamond,
        starting_point=-2,
        gauge=gauge_position_diamond,
    )
    print(result)


if __name__ == '__main__':
    main("input.txt")
