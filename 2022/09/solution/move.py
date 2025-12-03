import re

from direction import Direction


class Move:
    def __init__(self, move_string: str):
        move_match = re.match(r'([LRUD]) (\d{1,3})', move_string)
        self._direction = Direction.deserialize(move_match.group(1))
        self._distance = int(move_match.group(2))

    @property
    def steps(self):
        return [self._direction.value for _ in range(self._distance)]

    @property
    def normal(self):
        return self._direction.value.normal
