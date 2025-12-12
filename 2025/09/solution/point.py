from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __mul__(self, other: Point) -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
