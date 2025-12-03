from coordinate import Coordinate
from move import Move


class Rope:
    def __init__(self, length: int = 2):
        self._length = length
        self._tail_visits = set()
        self._positions = []
        self._step_count = 0

        for _ in range(length):
            self._positions.append(Coordinate(0, 0))

        self._tail_visits.add(self._positions[-1])

    def step(self, step: Coordinate):
        self._step_count += 1
        self._positions[0] += step

        for planck_length in range(1, self._length):
            self._positions[planck_length] = self.follow_previous_link(
                follower=self._positions[planck_length], leader=self._positions[planck_length - 1]
            )

        self._tail_visits.add(self._positions[-1])

    def move(self, move: Move):
        for step in move.steps:
            self.step(step)

    @staticmethod
    def links_touching(left: Coordinate, right: Coordinate):
        delta = left - right
        return abs(delta.x) <= 1 and abs(delta.y) <= 1

    @classmethod
    def follow_previous_link(cls, follower: Coordinate, leader: Coordinate):
        if cls.links_touching(follower, leader):
            return follower

        delta = (leader - follower)

        # if in same column or longer distance by Y axis
        if delta.x == 0 or abs(delta.x) < abs(delta.y):
            return Coordinate(leader.x, leader.y - 1 if delta.y > 0 else leader.y + 1)

        # if in same row or longer distance by X axis
        if delta.y == 0 or abs(delta.x) > abs(delta.y):
            return Coordinate(leader.x - 1 if delta.x > 0 else leader.x + 1, leader.y)

        return Coordinate(
            leader.x - 1 if delta.x > 0 else leader.x + 1,
            leader.y - 1 if delta.y > 0 else leader.y + 1
        )

    @property
    def tail_visit_count(self) -> int:
        return len(self._tail_visits)
