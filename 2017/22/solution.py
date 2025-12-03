from collections import defaultdict
from enum import Enum
from math import floor
from typing import Callable


class GridStates(Enum):
    CLEAN = "."
    WEAKENED = "w"
    FLAGGED = "f"
    INFECTED = "#"


class MovementDirection:
    UP = -1j
    DOWN = 1j
    LEFT = -1
    RIGHT = 1


class TurnDirection:
    LEFT = -1j
    RIGHT = 1j
    STAY = 1
    REVERSE = -1


class Grid(defaultdict):
    def __missing__(self, key):
        obj = GridStates.CLEAN
        self[key] = obj
        return obj


def initial_state_change(state: GridStates) -> GridStates:
    match state:
        case GridStates.CLEAN:
            return GridStates.INFECTED
        case _:
            return GridStates.CLEAN


def evolved_state_change(state: GridStates) -> GridStates:
    match state:
        case GridStates.CLEAN:
            return GridStates.WEAKENED
        case GridStates.WEAKENED:
            return GridStates.INFECTED
        case GridStates.INFECTED:
            return GridStates.FLAGGED
        case _:
            return GridStates.CLEAN


def direction_change(state: GridStates) -> complex:
    match state:
        case GridStates.CLEAN:
            return TurnDirection.LEFT
        case GridStates.INFECTED:
            return TurnDirection.RIGHT
        case GridStates.WEAKENED:
            return TurnDirection.STAY
        case _:
            return TurnDirection.REVERSE


def work(grid: Grid, start: complex, bursts: int, state_change: Callable[[GridStates], GridStates]) -> int:
    cycles = 0
    infections = 0

    position = start
    direction = MovementDirection.UP

    while cycles < bursts:
        cycles += 1

        direction *= direction_change(grid[position])
        new_state = state_change(grid[position])

        if new_state == GridStates.INFECTED:
            infections += 1

        grid[position] = new_state

        position += direction

    return infections


def main(filename: str, bursts_before_evolution: int, bursts_after_evolution: int):
    with open(filename) as f:
        rows = [_.strip() for _ in f.readlines()]

    grid = Grid()
    for n_row, row  in enumerate(rows):
        for n_column, column in enumerate(row):
            grid[n_column + n_row * 1j] = GridStates(column)

    mid_y = floor(len(rows) / 2)
    mid_x = floor(len(rows[mid_y]) / 2)
    position = mid_y + mid_x * 1j

    infections = work(
        grid=grid.copy(), start=position, bursts=bursts_before_evolution, state_change=initial_state_change
    )
    print(f"After {bursts_before_evolution} bursts {infections} habe infected a node.")

    evolved_infections = work(
        grid=grid.copy(), start=position, bursts=bursts_after_evolution, state_change=evolved_state_change
    )
    print(f"With the evolved virus {evolved_infections} burst cause an infection in {bursts_after_evolution} bursts.")


if __name__ == "__main__":
    main("test.txt", bursts_before_evolution=70, bursts_after_evolution=100)          # 41, 26
    main("test.txt", bursts_before_evolution=10000, bursts_after_evolution=10000000)  # 5587, 2511944
    main("input.txt", bursts_before_evolution=10000, bursts_after_evolution=10000000)
