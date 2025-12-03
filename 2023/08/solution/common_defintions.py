import re
from enum import Enum
from typing import List, Pattern, Union, Optional

PATTERN_TYPE = Union[str, Pattern[str]]


class Direction(Enum):
    LEFT = 'L'
    RIGHT = 'R'


class NodeDirections:
    def __init__(self, left: str, right: str):
        self._left = left
        self._right = right

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def __str__(self):
        return f'({self._left}, {self._right})'


class Node:
    def __init__(self, node_string: str):
        match = re.match(r'([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)', node_string)
        self._name = match.group(1)
        self._directions = NodeDirections(left=match.group(2), right=match.group(3))

    def __str__(self):
        return f'{self._name} -> {self._directions}'

    @property
    def name(self):
        return self._name

    def go(self, direction: Direction):
        if direction == Direction.LEFT:
            return self._directions.left
        return self._directions.right


class DirectionSet:
    def __init__(self, direction_string: str):
        self._directions = [Direction(_) for _ in direction_string.strip('\n')]
        self._length = len(self._directions)
        self._index = -1

    def __enter__(self):
        return self

    def __next__(self):
        self._index += 1
        return self._directions[self._index % self._length]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._index = -1


class Graph:
    def __init__(self, nodes: List[Node], start_node: str = 'AAA'):
        self._nodes = {_.name: _ for _ in nodes}
        self._current_node = None
        self.current_node = start_node
        self._start_node = start_node
        self._steps_taken = 0
        self._path = []

    @property
    def steps_taken(self):
        return self._steps_taken

    @property
    def start_node(self):
        return self._start_node

    @property
    def current_node(self):
        return self._current_node

    @current_node.setter
    def current_node(self, node: str):
        if node not in self._nodes:
            raise ValueError(f'`{node}` not in NodeList. Cannot start there.')
        self._current_node = node

    @property
    def path(self):
        return self._path

    def is_at_node(self, node: PATTERN_TYPE):
        return bool(re.match(node, self._current_node))

    def take_step(self, direction: Direction):
        self._path.append(self._current_node)
        self._current_node = self._nodes[self._current_node].go(direction)
        self._steps_taken += 1

    def find(self, target_node: str, direction_set: DirectionSet):
        if not any(re.match(target_node, _) for _ in self._nodes):
            raise ValueError(f'`{target_node}` not in NodeList. Cannot find that.')

        with direction_set as directions:
            while not self.is_at_node(target_node):
                self.take_step(next(directions))

    def reset(self, start_node: Optional[str] = 'AAA'):
        if start_node is None:
            start_node = self._start_node
        self.current_node = start_node
        self._start_node = start_node
        self._path = []
        self._steps_taken = 0
