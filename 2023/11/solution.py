from itertools import combinations

GALAXY_STRING = '#'


class Vector:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def expand_x(self, value: int = 1):
        self._x += value

    def expand_y(self, value: int = 1):
        self._y += value

    def __sub__(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            raise TypeError(f'Not implemented for type {type(other)}')

        return Vector(x=self._x - other.x, y=self._y - other.y)

    def __add__(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            raise TypeError(f'Not implemented for type {type(other)}')

        return Vector(x=self._x + other.x, y=self._y + other.y)

    def abs(self):
        return abs(self._x) + abs(self._y)


class Universe:
    def __init__(self, filename: str):
        _current_y = 0

        self._galaxies = []
        self._expand_rows = []

        with open(filename, 'r') as _f:
            universe_rows = _f.readlines()
            _dim_columns = len(universe_rows[0]) - 1

        for universe_row in universe_rows:
            universe_row.strip('\n')

            if GALAXY_STRING not in universe_row:
                self._expand_rows.append(_current_y)
            else:
                for point_index, point_str in enumerate(universe_row):
                    if point_str == GALAXY_STRING:
                        self._galaxies.append(Vector(x=point_index, y=_current_y))

            _current_y += 1

        self._expand_columns = [_ for _ in range(_dim_columns) if _ not in [__.x for __ in self._galaxies]]
        self._is_expanded = False
        self._cumulative_distance = None

    def expand(self, multiplier: int = 2):
        if self._is_expanded:
            return

        self._is_expanded = True
        previous_galaxies = self._galaxies
        self._galaxies = []

        for galaxy in previous_galaxies:
            dist_x = len([_ for _ in self._expand_columns if _ < galaxy.x])
            dist_y = len([_ for _ in self._expand_rows if _ < galaxy.y])

            galaxy.expand_y(dist_y * (multiplier - 1))
            galaxy.expand_x(dist_x * (multiplier - 1))

            self._galaxies.append(galaxy)

    @property
    def cumulative_distance(self):
        if self._cumulative_distance is None:
            _distance = 0
            for g1, g2 in combinations(self._galaxies, 2):
                _distance += (g1 - g2).abs()
            self._cumulative_distance = _distance
        return self._cumulative_distance


def main_part_1(filename: str):
    universe = Universe(filename)
    universe.expand()
    print(universe.cumulative_distance)


def main_part_2(filename: str):
    universe = Universe(filename)
    universe.expand(1000000)
    print(universe.cumulative_distance)


if __name__ == '__main__':
    main_part_1('./input.txt')
    main_part_2('./input.txt')
