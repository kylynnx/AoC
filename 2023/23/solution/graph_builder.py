from heapq import heappush, heappop
from typing import Tuple, List

from direction import Direction, allowed_directions, invert
from ground_type import GroundType, direction_from_slope


class GraphBuilder:
    def __init__(self, filename: str, graph_class, graph_class_keywords, set_edge_function):
        with open(filename, 'r') as _f:
            raw_lines = [_.strip('\n') for _ in _f.readlines()]

        self._dim_x = len(raw_lines[0])
        self._dim_y = len(raw_lines)

        self._slope_types = (GroundType.SLOPE_UP, GroundType.SLOPE_DOWN, GroundType.SLOPE_LEFT, GroundType.SLOPE_RIGHT)

        self._ground = []
        self._graph = graph_class(**graph_class_keywords)
        self._set_edge_function = staticmethod(set_edge_function)

        for line in raw_lines:
            for tile in line:
                self._ground.append(GroundType(tile))

        self.build_graph()

    def __contains__(self, item: Tuple[int, int]) -> bool:
        return 0 <= item[0] < self._dim_x and 0 <= item[1] < self._dim_y

    def _get_neighbors(self, position: Tuple[int, int], direction: Direction
                       ) -> Tuple[List[Tuple[Tuple[int, int], Direction]], bool]:
        if (ground_type := self._ground[self.get_lexic(position)]) in self._slope_types:
            new_direction = direction_from_slope(ground_type)
            new_position = (position[0] + new_direction.value[0], position[1] + new_direction.value[1])
            return [(new_position, new_direction)], False

        neighbors = []
        toggle_node = False

        for new_direction in allowed_directions[direction]:
            new_position = (position[0] + new_direction.value[0], position[1] + new_direction.value[1])

            if new_position not in self:
                continue

            if (ground_type := self._ground[self.get_lexic(new_position)]) != GroundType.WALL:
                if ground_type in self._slope_types:
                    if direction_from_slope(ground_type) == invert[new_direction]:
                        toggle_node = True
                        continue

                neighbors.append((new_position, new_direction))

        return neighbors, toggle_node

    def get_lexic(self, coordinate: Tuple[int, int]):
        return coordinate[0] + coordinate[1] * self._dim_x

    def build_graph(self):
        visited = set()
        _stack = []
        heappush(_stack, (self.start, self.start, Direction.DOWN))

        while _stack:
            position, path_start, direction = heappop(_stack)

            if (position, direction) in visited:
                continue

            visited.add((position, direction))

            steps = 0
            neighbors, _ = self._get_neighbors(position, direction)
            current_position = position
            while len(neighbors) == 1 and current_position != self.end:
                steps += 1
                current_position = neighbors[0][0]
                neighbors, toggle_node = self._get_neighbors(current_position, neighbors[0][1])

                if toggle_node:
                    break

            if current_position != self.end:
                for neighbor_position, new_direction in neighbors:
                    heappush(_stack, (neighbor_position, current_position, new_direction))

            if path_start != self.start:
                steps += 1

            self._set_edge_function(self._graph, path_start, current_position, steps)

    @property
    def graph(self):
        return self._graph

    @property
    def start(self):
        return 1, 0

    @property
    def end(self):
        return self._dim_x - 2, self._dim_y - 1
