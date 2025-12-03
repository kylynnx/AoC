from typing import Optional

from common_defintions import DirectionSet, Node, Graph, PATTERN_TYPE


class Map:
    def __init__(self, filename: str, start_node: str = 'AAA', target_node: PATTERN_TYPE = 'ZZZ'):
        with open(filename, 'r') as _f:
            direction_set = DirectionSet(_f.readline())
            _f.readline()
            nodes = [Node(_) for _ in _f.readlines()]
        graph = Graph(nodes=nodes, start_node=start_node)
        self._direction_set = direction_set
        self._graph = graph
        self._start_node = start_node
        self._target_node = target_node

    @property
    def steps_taken(self):
        return self._graph.steps_taken

    def reset(self, start_node: Optional[str] = None):
        if start_node is None:
            start_node = self._start_node
        self._graph.reset(start_node=start_node)
        self._start_node = start_node

    def get_steps_to(self, target_node: Optional[PATTERN_TYPE] = None) -> int:
        if target_node is None:
            target_node = self._target_node

        self._graph.find(target_node=target_node, direction_set=self._direction_set)
        steps = self.steps_taken
        self.reset()
        return steps


def main(filename: str):
    my_map = Map(filename)
    print(my_map.get_steps_to())


if __name__ == '__main__':
    main('../input.txt')
