from enum import Enum


def read_instructions(filename):
    with open(filename) as _f:
        return _f.readline()


class Instruction(Enum):
    UP = "("
    DOWN = ")"


def calculate_floor(instructions: str, start: int = 0) -> int:
    floor = start
    for step in instructions:
        if step == Instruction.UP.value:
            floor += 1
        else:
            floor -= 1

    return floor


def calculate_position_for_basement(instructions: str, start: int = 0, offset_position: int = 0) -> int:
    floor = start
    position = offset_position
    for step in instructions:
        position += 1
        if step == Instruction.UP.value:
            floor += 1
        else:
            floor -= 1

        if floor < 0:
            break

    return position


def main(filename: str):
    instructions = read_instructions(filename)
    print(calculate_floor(instructions))
    print(calculate_position_for_basement(instructions))


if __name__ == '__main__':
    main("input.txt")