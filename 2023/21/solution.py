from enum import Enum
from heapq import heappush, heappop


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class GardenMap:
    def __init__(self, filename: str):
        with open(filename, 'r') as _f:
            self._ground = [_.strip('\n') for _ in _f.readlines()]

        self._dim_y = len(self._ground)
        self._dim_x = len(self._ground[0])
        self._start = (self._dim_x // 2, self._dim_y // 2)

    @property
    def dim_x(self):
        return self._dim_x

    def count_reached_after_steps(self, steps: int):
        _visited = set()

        _stack = []
        heappush(_stack, (0, self._start))

        reached_count = 0

        while _stack:
            step_count, point = heappop(_stack)

            if point in _visited:
                continue

            _visited.add(point)

            if step_count % 2 == steps % 2:
                reached_count += 1

            if step_count >= steps:
                continue

            for direction in list(Direction):
                next_x, next_y = point[0] + direction.value[0], point[1] + direction.value[1]

                if self._ground[next_y % self._dim_y][next_x % self._dim_x] == '#':
                    continue

                heappush(_stack, (step_count + 1, (next_x, next_y)))

        return reached_count


def main(filename: str):
    garden_map = GardenMap(filename)
    print(garden_map.count_reached_after_steps(64))

    # Turns out the number of tiles reached grows quadratic in how many borders between two former maps are crossed.
    # A crossing happens every `dimension` steps. Apart from the first, as we are starting in the middle. Then all the
    # reached steps lie on the surface of a diamond shape. Taking the values at n, x+n, 2x+n one can fit the function
    # and evaluate at the target_value.

    steps = 26501365
    border_crossings = steps // garden_map.dim_x

    steps_0, steps_1, steps_2 = (
        garden_map.count_reached_after_steps(_ * garden_map.dim_x + (garden_map.dim_x // 2))
        for _ in range(3)
    )

    reached_count = (
        steps_0
        + border_crossings * (
            steps_1 - steps_0 + (
                (border_crossings - 1) * (
                    (steps_2 - 2 * steps_1 + steps_0) // 2
                )
            )
        )
    )

    print(reached_count)


if __name__ == '__main__':
    main('./input.txt')
