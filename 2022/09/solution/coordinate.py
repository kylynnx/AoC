from typing import Union


class Coordinate:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def __add__(self, other: 'Coordinate'):
        return Coordinate(self._x + other.x, self._y + other.y)

    def __sub__(self, other: 'Coordinate'):
        return Coordinate(self._x - other.x, self._y - other.y)

    def __eq__(self, other: 'Coordinate'):
        return self._x == other.x and self._y == other.y

    def __mul__(self, other: Union[int, 'Coordinate']):
        if isinstance(other, Coordinate):
            return self._x * other._x + self._y * other._y

        return Coordinate(self._x * other, self._y * other)

    def __hash__(self):
        return hash((self._x, self._y))
