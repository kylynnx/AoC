from enum import Enum

from coordinate import Coordinate


class Direction(Enum):
    LEFT = Coordinate(-1, 0)
    RIGHT = Coordinate(1, 0)
    UP = Coordinate(0, 1)
    DOWN = Coordinate(0, -1)

    @staticmethod
    def deserialize(direction_string: str) -> 'Direction':
        match direction_string:
            case 'R':
                return Direction.RIGHT
            case 'L':
                return Direction.LEFT
            case 'U':
                return Direction.UP
            case 'D':
                return Direction.DOWN
