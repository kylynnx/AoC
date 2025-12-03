import math
from typing import List


def modified_ceil(value: float) -> int:
    ceil_value = math.ceil(value)
    if value == ceil_value:
        ceil_value += 1

    return ceil_value


def modified_floor(value: float) -> int:
    floor_value = math.floor(value)
    if value == floor_value:
        floor_value -= 1

    return floor_value


class Race:
    def __init__(self, racing_time: int, record_distance: int):
        self._racing_time = racing_time
        self._record_distance = record_distance

    @property
    def winning_chances(self) -> int:
        half_time = self._racing_time * 0.5
        discriminant = math.sqrt(half_time * half_time - self._record_distance)
        left_time = modified_ceil(half_time - discriminant)
        right_time = modified_floor(half_time + discriminant)

        return right_time - left_time + 1


class Tournament:
    def __init__(self, racing_times: List[str], record_distances: List[str]):
        races = []
        for racing_time, record_distance in zip(racing_times, record_distances):
            races.append(Race(racing_time=int(racing_time), record_distance=int(record_distance)))

        self._races = races
        self._winning_chances = None

    @property
    def races(self):
        return self._races

    @property
    def race_winning_chances(self):
        return [_.winning_chances for _ in self._races]

    @property
    def cumulated_winning_chances(self):
        if not self._winning_chances:
            self._winning_chances = math.prod([_.winning_chances for _ in self._races])

        return self._winning_chances


def main(filename: str):
    with open(filename, 'r') as _f:
        racing_time_line = _f.readline()
        record_distance_line = _f.readline()

    part_01_racing_times = racing_time_line.split()[1:]
    part_01_record_distances = record_distance_line.split()[1:]
    tournament = Tournament(racing_times=part_01_racing_times, record_distances=part_01_record_distances)
    print(tournament.cumulated_winning_chances)

    part_02_racing_time = int(''.join(part_01_racing_times))
    part_02_record_distance = int(''.join(part_01_record_distances))
    race = Race(racing_time=part_02_racing_time, record_distance=part_02_record_distance)
    print(race.winning_chances)


if __name__ == '__main__':
    main('./input.txt')
