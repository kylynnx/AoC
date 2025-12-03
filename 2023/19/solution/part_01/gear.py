import re


class Gear:
    def __init__(self, gear_string: str):
        match = re.match(r'{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)}', gear_string)
        self._x = int(match.group(1))
        self._m = int(match.group(2))
        self._a = int(match.group(3))
        self._s = int(match.group(4))

    @property
    def x(self):
        return self._x

    @property
    def m(self):
        return self._m

    @property
    def a(self):
        return self._a

    @property
    def s(self):
        return self._s

    @property
    def xmas(self):
        return self._x + self._m + self._a + self._s
