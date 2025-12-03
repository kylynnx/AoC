import math
import re
from typing import List, Optional


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


class EnginePart:
    def __init__(self, coordinate: Coordinate, length: int):
        self._coordinate = coordinate
        self._length = length
        self._neighbors = []

    @property
    def length(self):
        return self._length

    @property
    def coordinate(self):
        return self._coordinate

    def _set_neighbors(self, engine: 'Engine'):
        self._neighbors = []
        x = self._coordinate.x
        y = self._coordinate.y
        if x > 0:
            x_start = x - 1
            self._neighbors.append(Coordinate(x=x_start, y=y))
        else:
            x_start = x

        if x + self._length - 1 < engine.max_x:
            x_end = x + self._length
            self._neighbors.append(Coordinate(x=x_end, y=y))
        else:
            x_end = x + self._length - 1

        if y > 0:
            for x in range(x_start, x_end + 1):
                self._neighbors.append(Coordinate(x=x, y=y-1))

        if y < engine.max_y:
            for x in range(x_start, x_end + 1):
                self._neighbors.append(Coordinate(x=x, y=y+1))


class Engine:
    def __init__(self, filename: str):
        with open(filename, 'r') as _f:
            self._config = _f.readlines()

        self._dim_x = len(self._config[0]) - 1
        self._dim_y = len(self._config)

        self._numbers: List[PartNumber] = []
        self._find_numbers()

        self._parts: List[PartNumber] = []

        self._specials: List[Gear] = []
        self._find_gear_candidates()

        self._gears: List[Gear] = []

    @property
    def max_x(self):
        return self._dim_x - 1

    @property
    def max_y(self):
        return self._dim_y - 1

    @property
    def parts(self):
        if not self._parts:
            self._parts = [_ for _ in self._numbers if _.is_part(self)]
        return self._parts

    @property
    def gears(self):
        if not self._gears:
            self._gears = [_ for _ in self._specials if _.is_gear(self)]
        return self._gears

    def get(self, coordinate: Coordinate) -> str:
        return self._config[coordinate.y][coordinate.x]

    def get_part_number(self, coordinate: Coordinate) -> Optional['PartNumber']:
        for part in self.parts:
            part_x_start = part.coordinate.x
            part_x_end = part_x_start + part.length - 1
            part_y = part.coordinate.y
            if coordinate.y == part_y and part_x_start <= coordinate.x <= part_x_end:
                return part

        return None

    def _find_numbers(self):
        for index_y, config_line in enumerate(self._config):
            index_x = 0
            while index_x <= self.max_x:
                if not config_line[index_x].isdigit():
                    index_x += 1
                else:
                    if index_x == self.max_x:
                        if config_line[index_x].isdigit():
                            self._numbers.append(
                                PartNumber(
                                    value=int(config_line[index_x]),
                                    coordinate=Coordinate(x=index_x, y=index_y),
                                    length=1
                                )
                            )
                            break
                    else:
                        end = index_x + 1
                        while end <= self.max_x + 1:
                            if not config_line[index_x:end].isnumeric():
                                break
                            end += 1
                        if index_x == end - 1:
                            value = config_line[index_x:]
                        else:
                            value = config_line[index_x: end - 1]
                        self._numbers.append(
                            PartNumber(
                                value=int(value),
                                coordinate=Coordinate(x=index_x, y=index_y),
                                length=end - index_x - 1
                            )
                        )
                        index_x = end

    def _find_gear_candidates(self):
        for index_y, config_line in enumerate(self._config):
            for index_x, config_str in enumerate(config_line):
                if re.match(r'\*', config_str):
                    self._specials.append(Gear(coordinate=Coordinate(x=index_x, y=index_y)))


class PartNumber(EnginePart):
    def __init__(self, value: int, coordinate: Coordinate, length: int):
        super().__init__(coordinate=coordinate, length=length)
        self._value = value
        self._is_part = None

    @property
    def value(self):
        return self._value

    def is_part(self, engine: Engine):
        self._set_neighbors(engine)
        if self._is_part is None:
            self._is_part = False
            for neighbor in self._neighbors:
                if re.match(r'[^0-9.]', engine.get(neighbor)):
                    self._is_part = True
        return self._is_part


class Gear(EnginePart):
    def __init__(self, coordinate: Coordinate):
        super().__init__(coordinate=coordinate, length=1)
        self._gear_ratio = 0
        self._is_gear = None

    @property
    def gear_ratio(self) -> int:
        return self._gear_ratio

    def is_gear(self, engine: Engine) -> bool:
        self._set_neighbors(engine)
        if self._is_gear is None:
            self._is_gear = False
            neighbor_parts = set()
            for neighbor in self._neighbors:
                if part := engine.get_part_number(neighbor):
                    neighbor_parts.add(part)
            if len(neighbor_parts) == 2:
                self._gear_ratio = math.prod([_.value for _ in neighbor_parts])
                self._is_gear = True
        return self._is_gear


def main(filename: str):
    engine = Engine(filename)
    parts = engine.parts

    print(sum([_.value for _ in parts]))

    gears = engine.gears
    print(sum([_.gear_ratio for _ in gears]))


if __name__ == '__main__':
    main('./input.txt')
