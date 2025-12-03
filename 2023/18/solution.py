import re
from enum import Enum
from typing import Tuple, List, Callable


class Coordinate:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __add__(self, other: 'Coordinate'):
        return Coordinate(x=self._x + other.x, y=self._y + other.y)

    def __mul__(self, other: int):
        return Coordinate(x=self._x * other, y=self._y * other)


class Direction(Enum):
    L = Coordinate(x=-1, y=0)
    R = Coordinate(x=1, y=0)
    U = Coordinate(x=0, y=1)
    D = Coordinate(x=0, y=-1)


def get_direction(direction: str) -> Direction:
    match direction:
        case '0':
            return Direction.R
        case '1':
            return Direction.D
        case '2':
            return Direction.L
        case '3':
            return Direction.U


def deserialize_line(line: str) -> Tuple[Direction, int]:
    match = re.match(r'([LRUD]) ([0-9]{1,2})', line)
    return Direction[match.group(1)], int(match.group(2))


def hex_line(line: str) -> Tuple[Direction, int]:
    match = re.match(r'[LRUD] [0-9]{1,2} \(#([0-9a-f]{5})([0-9a-f])\)', line)
    distance = int(match.group(1), 16)
    direction = get_direction(match.group(2))
    return direction, distance


def transform_nodes(nodes: List[Coordinate]) -> List[Coordinate]:
    min_x = min(_.x for _ in nodes)
    min_y = min(_.y for _ in nodes)

    offset = Coordinate(
        x=min_x if min_x < 0 else 0,
        y=min_y if min_y < 0 else 0
    )
    offset *= -1

    area_nodes = [_ + offset for _ in nodes]
    area_nodes.reverse()

    return area_nodes


def determine_area(nodes: List[Coordinate]) -> int:
    internal_area = 0
    circumference = 0
    current_coordinate = nodes[0]

    for next_coordinate in nodes[1:]:
        circumference += abs(current_coordinate.x - next_coordinate.x)
        circumference += abs(current_coordinate.y - next_coordinate.y)

        internal_area += current_coordinate.x * next_coordinate.y
        internal_area -= current_coordinate.y * next_coordinate.x

        current_coordinate = next_coordinate

    internal_area += current_coordinate.x * nodes[0].y
    internal_area -= current_coordinate.y * nodes[0].x

    circumference += abs(current_coordinate.x - nodes[0].x)
    circumference += abs(current_coordinate.y - nodes[0].y)

    area = (internal_area + circumference) // 2 + 1
    return area


def main(filename: str, line_function: Callable[[str], Tuple[Direction, int]]):
    _previous = Coordinate(x=0, y=0)
    nodes = []

    with open(filename, 'r') as _f:
        for line in _f.readlines():
            direction, length = line_function(line)
            _previous = _previous + (direction.value * length)
            nodes.append(_previous)

    area_nodes = transform_nodes(nodes)

    print(determine_area(area_nodes))


if __name__ == '__main__':
    main('./input.txt', line_function=deserialize_line)
    main('./input.txt', line_function=hex_line)
