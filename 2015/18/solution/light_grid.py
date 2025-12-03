from utility import LightState


class LightGrid:
    def __init__(self, filename: str):
        with open(filename) as f:
            rows = [_.strip("\n") for _ in f.readlines()]

        self._dim_y = len(rows)
        self._dim_x = len(rows[0])

        self._grid = []
        for row in rows:
            for light in row:
                self._grid.append(light == LightState.ON.value)

        self._set_corners_on()

    @property
    def dim_x(self):
        return self._dim_x

    @property
    def dim_y(self):
        return self._dim_y

    @property
    def grid(self):
        return self._grid

    @property
    def light_count(self):
        return sum(self._grid)

    def get_row(self, y: int) -> list[bool]:
        if not 0 <= y < self._dim_y:
            raise ValueError()

        return self._grid[y * self._dim_x: (y + 1) * self._dim_x]

    def get_cell(self, x: int, y: int) -> bool:
        if not 0 <= y < self._dim_y:
            raise ValueError()

        if not 0 <= x < self._dim_x:
            raise ValueError()

        return self._grid[y * self._dim_x + x]

    def _set_corners_on(self):
        self._grid[0] = True
        self._grid[-1] = True
        self._grid[self._dim_x - 1] = True
        self._grid[self._dim_y * (self._dim_x - 1)] = True

    def advance(self, steps: int, stuck_corners: bool = False):
        for _ in range(steps):
            self.advance_single_step(stuck_corners)

    def advance_single_step(self, stuck_corners: bool = False):
        next_grid = [False] * self._dim_x * self._dim_y

        for x in range(self._dim_x):
            for y in range(self._dim_y):
                adjacents = [
                    (x + 1, y + 1),
                    (x + 1, y),
                    (x + 1, y - 1),
                    (x, y + 1),
                    (x, y - 1),
                    (x - 1, y + 1),
                    (x - 1, y),
                    (x - 1, y - 1),
                ]

                alive_neighbors = 0

                for adjacent_x, adjacent_y in adjacents:
                    if not 0 <= adjacent_x < self._dim_x or not 0 <= adjacent_y < self._dim_y:
                        continue

                    alive_neighbors += self._grid[adjacent_y * self._dim_x + adjacent_x]

                state_at_current_position = self._grid[y * self._dim_x + x]

                if state_at_current_position and 2 <= alive_neighbors <= 3:
                    next_grid[y * self._dim_x + x] = True
                elif not state_at_current_position and alive_neighbors == 3:
                    next_grid[y * self._dim_x + x] = True

        self._grid = next_grid
        if stuck_corners:
            self._set_corners_on()
