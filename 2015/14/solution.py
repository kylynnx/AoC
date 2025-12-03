import re


class Reindeer:
    def __init__(self, reindeer_string: str):
        match = re.match(
            r"([a-zA-z]+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.",
            reindeer_string
        )
        self._name = match.group(1)
        self._velocity = int(match.group(2))
        self._fly_time = int(match.group(3))
        self._rest_time = int(match.group(4))

    @property
    def name(self):
        return self._name

    def get_distance_in_time(self, seconds: int) -> int:
        full_cycles = seconds // (self._fly_time + self._rest_time)

        distance = self._fly_time * self._velocity * full_cycles

        remaining_seconds = seconds - full_cycles * (self._fly_time + self._rest_time)

        distance += min(remaining_seconds, self._fly_time) * self._velocity

        return distance


def main(filename: str, race_time: int):
    reindeers = {}
    with open(filename) as f:
        for line in f.readlines():
            _rr = Reindeer(line)
            reindeers[_rr.name] = _rr

    distances = [_.get_distance_in_time(race_time) for _ in reindeers.values()]

    print(max(distances))

    reindeer_points = {_: 0 for _ in reindeers}
    for timestamp in range(1, race_time + 1):
        distances = {}
        for name, reindeer in reindeers.items():
            distances[name] = reindeer.get_distance_in_time(timestamp)
        max_distance = max(distances.values())
        for name in reindeer_points:
            if distances[name] == max_distance:
                reindeer_points[name] += 1

    print(reindeer_points)


if __name__ == "__main__":
    main("input.txt", 2503)
