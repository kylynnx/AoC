import string
from enum import Enum


class Direction(Enum):
    DOWN = (1, 0)
    UP = (-1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


def main(filename: str):
    with open(filename) as f:
        grid = [[node for node in row.strip("\n")] + [" "] for row in f.readlines()]

    max_length = max(len(row) for row in grid)

    for idx in range(len(grid)):
        grid[idx] += [" "] * (max_length - len(grid[idx]))

    column = grid[0].index("|")
    row = 0
    direction = Direction.DOWN

    path, steps = walk(grid=grid, start_row=row, start_column=column, direction=direction)
    print(f"The package walks the path {path} in {steps} steps.")


def walk(grid: list[list[str]], start_row: int, start_column: int, direction: Direction) -> tuple[str, int]:
    path = ""
    steps = 0

    row = start_row
    column = start_column
    toggle = True

    while toggle:
        row, column, direction, part, toggle = step(grid=grid, row=row, column=column, direction=direction)
        path += part
        steps += 1

    return path, steps


def step(grid: list[list[str]], row: int, column: int, direction: Direction) -> tuple[int, int, Direction, str, bool]:
    row += direction.value[0]
    column += direction.value[1]
    part = ""

    node = grid[row][column]

    if node == "+":
        direction = turn(grid=grid, direction=direction, row=row, column=column)
    elif node in string.ascii_uppercase:
        part = node

    return row, column, direction, part, node != " "


def turn(grid: list[list[str]], direction: Direction, row: int, column: int) -> Direction:
    if direction in (Direction.UP, Direction.DOWN):
        return turn_horizontally(grid=grid, row=row, column=column)

    return turn_vertically(grid=grid, row=row, column=column)


def turn_horizontally(grid: list[list[str]], row: int, column: int) -> Direction:
    left = grid[row][column - 1]

    if left != " ":
        return Direction.LEFT

    return Direction.RIGHT


def turn_vertically(grid: list[list[str]], row: int, column: int) -> Direction:
    up = grid[row - 1][column]

    if up != " ":
        return Direction.UP

    return Direction.DOWN


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
