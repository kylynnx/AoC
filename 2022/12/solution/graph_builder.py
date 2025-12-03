from typing import Tuple, List

from dijkstar import Graph


class GraphBuilder:
    def __init__(self, filename: str, start_elevation: int = 0, target_elevation: int = 25) -> None:
        with open(filename) as _f:
            self._hill = [_.strip('\n') for _ in _f.readlines()]

        self._number_hill = []
        self._dim_x = len(self._hill[0])
        self._dim_y = len(self._hill)
        self._start_elevation = start_elevation
        self._target_elevation = target_elevation
        self._optional_starts = None

    def build(self) -> Tuple[Graph, Tuple[int, int], Tuple[int, int]]:
        graph = Graph(undirected=False)

        start, target = self._find_start_and_target()
        self._set_number_hill(start=start, target=target)

        for y in range(self._dim_y):
            for x in range(self._dim_x):
                for neighbor in self._get_neighbors(x=x, y=y):
                    graph.add_edge((x, y), neighbor, 1)

        return graph, start, target

    def _find_start_and_target(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        start = None
        target = None

        y = 0
        while start is None or target is None:
            if 'S' in self._hill[y]:
                start = (self._hill[y].index('S'), y)
            if 'E' in self._hill[y]:
                target = (self._hill[y].index('E'), y)
            y += 1

        return start, target

    def _set_number_hill(self, start: Tuple[int, int], target: Tuple[int, int]):
        for hill_line in self._hill:
            self._number_hill.append([ord(_) - ord('a') for _ in hill_line])

        self._number_hill[start[1]][start[0]] = self._start_elevation
        self._number_hill[target[1]][target[0]] = self._target_elevation

    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        allowed_neighbors = []

        height = self._number_hill[y][x]

        if x > 0 and self._number_hill[y][x-1] <= height + 1:
            allowed_neighbors.append((x-1, y))

        if x < self._dim_x - 1 and self._number_hill[y][x+1] <= height + 1:
            allowed_neighbors.append((x+1, y))

        if y > 0 and self._number_hill[y-1][x] <= height + 1:
            allowed_neighbors.append((x, y-1))

        if y < self._dim_y - 1 and self._number_hill[y+1][x] <= height + 1:
            allowed_neighbors.append((x, y+1))

        return allowed_neighbors

    @property
    def optional_starts(self):
        if self._optional_starts is None:
            self._optional_starts = []
            for x in range(self._dim_x):
                for y in range(self._dim_y):
                    if self._number_hill[y][x] == self._start_elevation:
                        self._optional_starts.append((x, y))

        return self._optional_starts
