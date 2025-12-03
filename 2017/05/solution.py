from copy import copy
from typing import Callable


def main(filename: str):
    with open(filename) as f:
        instructions = [int(_.strip("\n")) for _ in f.readlines()]
    steps = execute_instructions(copy(instructions), increase)
    print(f"It takes {steps} steps to reach the exit.")

    steps = execute_instructions(instructions, decrease_large_values_increase_small)
    print(f"It takes {steps} steps to reach the exit when decreasing large values.")


def increase(value: int) -> int:
    return value + 1


def decrease_large_values_increase_small(value: int) -> int:
    if value >= 3:
        return value - 1

    return value + 1

def execute_instructions(instructions: list[int], update_function: Callable[[int], int]) -> int:
    steps = 0
    pointer = 0

    while 0 <= pointer < len(instructions):
        steps += 1
        jump_offset = instructions[pointer]
        instructions[pointer] = update_function(jump_offset)
        pointer += jump_offset

    return steps

if __name__ == "__main__":
    main("input.txt")
