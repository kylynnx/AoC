from typing import Tuple


class HeatLossMap:
    def __init__(self, filename: str):
        self._points = []
        with open(filename, 'r') as _f:
            _raw_lines = [_.strip('\n') for _ in _f.readlines()]

        self._dim_y = len(_raw_lines)
        self._dim_x = len(_raw_lines[0])

        for line in _raw_lines:
            for point in line:
                self._points.append(int(point))

    @property
    def dim_x(self):
        return self._dim_x

    @property
    def dim_y(self):
        return self._dim_y

    def __contains__(self, item: Tuple[int, int]):
        return 0 <= item[0] < self._dim_x and 0 <= item[1] < self._dim_y and item[0] + item[1] > 0

    def to_lexic(self, coordinate: Tuple[int, int]):
        return (coordinate[1] * self._dim_x) + coordinate[0]

    def get_heat_loss(self, coordinate: Tuple[int, int]) -> int:
        return self._points[self.to_lexic(coordinate)]
