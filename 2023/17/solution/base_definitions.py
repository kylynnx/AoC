from enum import Enum
from typing import Tuple


class Direction(Enum):
    LEFT = (-1, 0, 0)
    RIGHT = (1, 0, 1)
    UP = (0, -1, 2)
    DOWN = (0, 1, 3)


def rotate_direction(direction: Direction) -> Tuple[Direction, Direction]:
    match direction:
        case Direction.UP | Direction.DOWN:
            return Direction.LEFT, Direction.RIGHT
        case Direction.LEFT | Direction.RIGHT:
            return Direction.UP, Direction.DOWN
