from itertools import combinations

from line import Line
from point import Point


class Polygon:
    def __init__(self, points: list[Point]):
        self._points = points
        self._perimeter: set[Point] = set()

        for n in range(len(points)):
            start = points[n]
            end = points[(n + 1) % len(points)]
            self._perimeter.update(Line(start, end).points)

        self._areas = [((p, q), p * q) for p, q in combinations(self._points, 2)]
        self._areas.sort(key=lambda x: x[1], reverse=True)

    def get_max_area(self, inscribed: bool = False) -> int:
        for pair, area in self._areas:
            if not inscribed:
                return area

            diagonal = Line(*pair)

            if not any(_ in diagonal for _ in self._perimeter):
                return area

        return 0
