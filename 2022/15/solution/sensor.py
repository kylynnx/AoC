import re
from typing import Tuple, Optional


class Sensor:
    def __init__(self, sensor_line: str):
        sensor_match = re.match(
            r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)',
            sensor_line
        )

        self._sensor_x = int(sensor_match.group(1))
        self._sensor_y = int(sensor_match.group(2))

        self._beacon_x = int(sensor_match.group(3))
        self._beacon_y = int(sensor_match.group(4))

        self._closest_distance = abs(self._sensor_x - self._beacon_x) + abs(self._sensor_y - self._beacon_y)

    def get_forbidden_beacon_position_range(
            self, y: int, lower_bound: Optional[int] = None, upper_bound: Optional[int] = None) -> Optional[Tuple[int, int]]:
        constant_x = self._closest_distance - abs(self._sensor_y - y)

        if constant_x < 0:
            return None

        negative_solution = self._sensor_x - constant_x
        positive_solution = self._sensor_x + constant_x

        min_x = min(negative_solution, positive_solution)
        max_x = max(negative_solution, positive_solution)

        if lower_bound is not None and upper_bound is not None:
            if min_x < lower_bound:
                if max_x < lower_bound:
                    return None
                min_x = lower_bound

            if max_x > upper_bound:
                if min_x > upper_bound:
                    return None
                max_x = upper_bound

        return min_x, max_x

    @property
    def sensor_position(self) -> Tuple[int, int]:
        return self._sensor_x, self._sensor_y

    @property
    def beacon_position(self) -> Tuple[int, int]:
        return self._beacon_x, self._beacon_y
