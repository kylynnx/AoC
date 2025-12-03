from typing import Optional


class Cave:
    def __init__(self, filename: str):
        with open(filename, 'r') as _f:
            scan_lines = [_.strip('\n') for _ in _f.readlines()]

        self._rocks = set()
        self._sand = set()
        for line in scan_lines:
            self._deserialize_rocks(line)

        self._max_y = max(_.imag for _ in self._rocks)
        self._floor_y = None

    def __contains__(self, item):
        return item in self._rocks or item in self._sand

    @property
    def sand_count(self):
        return len(self._sand)

    def _deserialize_rocks(self, scan_line: str):
        points = [tuple(int(__) for __ in _.split(',')) for _ in scan_line.split(' -> ')]
        for p1, p2 in zip(points[:-1], points[1:]):
            p1x, p1y = p1
            p2x, p2y = p2

            if p1x == p2x:
                self._deserialize_vertical(base=p1x, start=min(p1y, p2y), end=max(p1y, p2y) + 1)
            else:
                self._deserialize_horizontal(height=p1y, start=min(p1x, p2x), end=max(p1x, p2x) + 1)

    def _deserialize_vertical(self, base: int, start: int, end: int):
        for y in range(start, end):
            self._rocks.add(base + y * 1j)

    def _deserialize_horizontal(self, height: int, start: int, end: int):
        for x in range(start, end):
            self._rocks.add(x + height * 1j)

    def _next_step(self, position):
        for dx in (0, -1, 1):
            if position + dx not in self:
                return position + dx

        return None

    def _add_sand(self, start_point: Optional[complex] = None, ground_level: Optional[int] = None) -> complex:
        if start_point is None:
            start_point = 500

        if ground_level is None:
            ground_level = self._max_y

        current_position = start_point
        next_position = self._next_step(current_position + 1j)
        while next_position is not None and next_position.imag <= ground_level:
            current_position = next_position
            next_position = self._next_step(current_position + 1j)

        self._sand.add(current_position)

        return current_position

    def fill_bottomless(self, start_point: Optional[complex] = None):
        is_contained = True
        while is_contained:
            added_sand = self._add_sand(start_point=start_point)

            if added_sand.imag >= self._max_y:
                is_contained = False

    def fill(self, start_point: Optional[complex] = None, floor_offset: Optional[int] = 1):
        entrance_blocked = False
        self._sand = set()
        while not entrance_blocked:
            added_sand = self._add_sand(start_point=start_point, ground_level=self._max_y + floor_offset)

            if added_sand == 500:
                entrance_blocked = True
