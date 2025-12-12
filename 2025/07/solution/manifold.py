from collections import defaultdict
from enum import Enum


from beam_splitter import BeamSplitter


class ManifoldType(Enum):
    SOURCE = "S"
    EMPTY = "."
    BEAM_SPLITTER = "^"


class Manifold:
    def __init__(self, filename: str):
        with open(filename) as f:
            content = [_.strip() for _ in f.readlines()]

        self._manifold = {}
        self._dim_y = len(content)
        self._beam_splitters = {}
        self._timelines = 0

        self.source_position = 0
        for y, line in enumerate(content):
            for x, position in enumerate(line):
                if position == ManifoldType.SOURCE.value:
                    self.source_position = x + y * 1j
                elif position == ManifoldType.BEAM_SPLITTER.value:
                    self._beam_splitters[x + y * 1j] = BeamSplitter()

        self._trace()

    def _trace(self):
        timelines_to_reach = defaultdict(int)
        timelines_to_reach[self.source_position] = 1

        for depth in range(self._dim_y):
            sources = [(position, timelines) for position, timelines in timelines_to_reach.items() if position.imag == depth]

            for position, timelines in sources:
                down = position + 1j

                if down in self._beam_splitters:
                    self._beam_splitters[down].activate()

                    for horizontal in (-1, 1):
                        timelines_to_reach[down + horizontal] += timelines
                else:
                    timelines_to_reach[down] += timelines

        self._timelines = sum(
            timelines for position, timelines in timelines_to_reach.items() if position.imag == self._dim_y
        )

    @property
    def active_beam_splitters(self):
        return sum(_.is_active for _ in self._beam_splitters.values())

    @property
    def timelines(self):
        return self._timelines
