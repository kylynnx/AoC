from typing import Sized


class Lights(Sized):
    def __init__(self, values: list[bool]):
        self._values = values

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:
        return "".join("#" if _ else "." for _ in self._values)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __iter__(self):
        return iter(self._values)

    def __eq__(self, other: Lights) -> bool:
        return self._values == other.values

    def __lt__(self, other: Lights) -> bool:
        return sum(self._values) < sum(other._values)

    @property
    def numeric(self):
        return sum(int(_) * (2 ** idx) for idx, _ in enumerate(self._values))

    @property
    def values(self) -> list[bool]:
        return self._values

    def distance(self, other: Lights) -> int:
        return sum(abs(o - s) for o, s in zip(self.values, other.values))
