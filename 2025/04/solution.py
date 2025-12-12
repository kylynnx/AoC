from collections import defaultdict
from enum import Enum


class PositionType(Enum):
    EMPTY = "."
    PAPER_ROLL = "@"


class Directions(Enum):
    NORTH = -1j
    SOUTH = 1j
    WEST = -1
    EAST = 1
    NORTH_WEST = 1 - 1j
    NORTH_EAST = -1 - 1j
    SOUTH_WEST = -1 + 1j
    SOUTH_EAST = 1 + 1j


class Cafeteria(defaultdict):
    def __missing__(self, key: complex):
        item = PositionType.EMPTY
        self[key] = item

        return item

    def check_position_forklift_accessible(self, position: complex) -> bool:
        neighboring_rolls = sum(self[position + _.value] == PositionType.PAPER_ROLL for _ in Directions)
        return neighboring_rolls < 4

    def get_forklift_accessible_rolls(self) -> list[complex]:
        accessible_rolls = []

        iterator = list(self.items())

        for position, position_type in iterator:
            if position_type == PositionType.EMPTY:
                continue

            if self.check_position_forklift_accessible(position):
                accessible_rolls.append(position)

        return accessible_rolls

    def remove_accessible_rolls(self, rolls: list[complex]) -> None:
        for position in rolls:
            self[position] = PositionType.EMPTY


def main(filename: str):
    with open(filename) as f:
        lines = [_.strip() for _ in f.readlines()]

    cafeteria = Cafeteria()

    for y, line in enumerate(lines):
        for x, position in enumerate(line):
            cafeteria[x + y * 1j] = PositionType(position)

    forklift_accessible_rolls = cafeteria.get_forklift_accessible_rolls()
    print(f"In this cafeteria {len(forklift_accessible_rolls)} are forklift accessible.")

    removed_rolls = 0
    while forklift_accessible_rolls:
        removed_rolls += len(forklift_accessible_rolls)
        cafeteria.remove_accessible_rolls(forklift_accessible_rolls)
        forklift_accessible_rolls = cafeteria.get_forklift_accessible_rolls()
    print(f"In total {removed_rolls} rolls can be removed.")


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
