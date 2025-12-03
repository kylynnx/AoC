from enum import Enum

from direction import Direction


class GroundType(Enum):
    WALL = '#'
    GROUND = '.'
    SLOPE_LEFT = '<'
    SLOPE_RIGHT = '>'
    SLOPE_UP = '^'
    SLOPE_DOWN = 'v'


def direction_from_slope(slope: GroundType) -> Direction:
    match slope:
        case GroundType.SLOPE_LEFT:
            return Direction.LEFT
        case GroundType.SLOPE_RIGHT:
            return Direction.RIGHT
        case GroundType.SLOPE_DOWN:
            return Direction.DOWN

    return Direction.UP
