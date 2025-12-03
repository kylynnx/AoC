import math
import re
from typing import Optional

from common_defintions import DirectionSet, Node, Graph, PATTERN_TYPE


class MapEnsemble:
    def __init__(self, filename: str, start_regex: PATTERN_TYPE = '[A-Z]{2}A',
                 target_regex: PATTERN_TYPE = '[A-Z]{2}Z'):
        with open(filename, 'r') as _f:
            direction_set = DirectionSet(_f.readline())
            _f.readline()
            nodes = [Node(_) for _ in _f.readlines()]

        self._direction_set = direction_set
        start_nodes = [_.name for _ in nodes if re.match(start_regex, _.name)]
        self._graphs = [Graph(nodes=nodes, start_node=_) for _ in start_nodes]
        self._target_regex = target_regex

    def find_least_common_steps_to(self, target_regex: Optional[PATTERN_TYPE] = None):
        if target_regex is None:
            target_regex = self._target_regex

        trips = []
        for graph in self._graphs:

            graph.find(target_node=target_regex, direction_set=self._direction_set)
            _steps_to_target = graph.steps_taken
            graph.reset(None)

            trips.append(_steps_to_target)

        return math.lcm(*trips)

    def reset(self):
        for graph in self._graphs:
            graph.reset(None)


def main(filename: str):
    my_ensemble = MapEnsemble(filename)
    print(my_ensemble.find_least_common_steps_to())


if __name__ == '__main__':
    main('../input.txt')
