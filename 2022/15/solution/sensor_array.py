import operator
from typing import Tuple, List, Optional, Set

from sensor import Sensor


class SensorArray:
    def __init__(self, filename: str):
        with open(filename) as _f:
            sensor_lines = _f.readlines()

        self._sensors = [Sensor(_) for _ in sensor_lines]

    def get_forbidden_beacon_ranges(
            self, y: int, lower_bound: Optional[int] = None, upper_bound: Optional[int] = None) -> List[Tuple[int, int]]:
        forbidden_position_ranges = []

        for sensor in self._sensors:
            new_range = sensor.get_forbidden_beacon_position_range(y, lower_bound=lower_bound, upper_bound=upper_bound)
            if new_range:
                forbidden_position_ranges.append(new_range)

        return self._collapse_ranges(forbidden_position_ranges)

    def count_forbidden_beacon_positions(
            self, y: int, lower_bound: Optional[int] = None, upper_bound: Optional[int] = None,
            exclude_beacons: Optional[bool] = True) -> int:
        collapsed_ranges = self.get_forbidden_beacon_ranges(y=y, lower_bound=lower_bound, upper_bound=upper_bound)

        count_forbidden = 0

        for start, end in collapsed_ranges:
            count_forbidden += abs(end - start) + 1

        if exclude_beacons:
            count_forbidden -= len(self.get_beacons_at(y=y, lower_bound=lower_bound, upper_bound=upper_bound))

        return count_forbidden

    @staticmethod
    def _collapse_ranges(old_ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        old_ranges = sorted(old_ranges, key=operator.itemgetter(0))
        new_ranges = []

        current_start, current_end = old_ranges[0]

        for old_range in old_ranges[1:]:
            if current_start is None:
                current_start, current_end = old_range
                continue

            start, end = old_range
            if start <= current_end:
                if end > current_end:
                    current_end = end
            else:
                new_ranges.append((current_start, current_end))
                current_start, current_end = start, end

        new_ranges.append((current_start, current_end))

        return new_ranges

    def get_beacons_at(self, y: int, lower_bound: Optional[int] = None, upper_bound: Optional[int] = None) -> Set[int]:
        if lower_bound is not None and upper_bound is not None:
            return set(
                _.beacon_position[0] for _ in self._sensors
                if _.beacon_position[1] == y and lower_bound <= _.beacon_position[0] <= upper_bound
            )
        else:
            return set(_.beacon_position[0] for _ in self._sensors if _.beacon_position[1] == y)

    def find_allowed_beacon_coordinates(self, lower_bound: int, upper_bound: int) -> Tuple[int, int]:
        allowed_range = range(lower_bound, upper_bound + 1)
        len_allowed_range = len(allowed_range)

        for y in allowed_range:
            forbidden_length = self.count_forbidden_beacon_positions(
                y=y, lower_bound=lower_bound, upper_bound=upper_bound, exclude_beacons=False
            )

            if forbidden_length != len_allowed_range:
                forbidden_ranges = [
                    range(_, __ + 1) for _, __ in self.get_forbidden_beacon_ranges(
                        y=y, lower_bound=lower_bound, upper_bound=upper_bound
                    )
                ]

                beacon_positions = self.get_beacons_at(y=y, lower_bound=lower_bound, upper_bound=upper_bound)

                x = lower_bound
                while x <= upper_bound:
                    if x in beacon_positions or any(x in _ for _ in forbidden_ranges):
                        x += 1
                        continue
                    return x, y

        return 0, 0

