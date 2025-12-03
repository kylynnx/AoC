from collections import defaultdict
from heapq import heappush, heappop
from itertools import combinations
from typing import Dict, List, Optional, Tuple
from dijkstar import Graph, find_path

from valve import Valve


class ValveSystem:
    def __init__(self, filename: str, start_node: str = 'AA', max_time: int = 30, plan_time: int = 4):
        self._start_node = start_node
        self._max_time = max_time
        self._elephant_max_time = max_time - plan_time
        with open(filename, 'r') as _f:
            configs = [_.strip('\n') for _ in _f.readlines()]

        self._valves: Dict[str, Valve] = {}
        self._non_broken_valves = set()
        self._deserialize_valves(configs)

        self._simple_graph: Optional[Graph] = None
        self._construct_simple_graph()

        self._valve_map = defaultdict(set)
        self._build_valve_map()

    def _deserialize_valves(self, valve_configs: List[str]):
        for valve_config in valve_configs:
            _valve = Valve(valve_config)

            if _valve.flow_rate:
                self._non_broken_valves.add(_valve.name)
            self._valves[_valve.name] = _valve

    def _construct_simple_graph(self):
        self._simple_graph = Graph(undirected=True)

        for valve_name, valve in self._valves.items():
            for neighbor in valve.tunnels:
                self._simple_graph.add_edge(valve_name, neighbor, 1)

    def _build_valve_map(self):
        if self._start_node not in self._non_broken_valves:
            for valve_name in self._non_broken_valves:
                self._set_valve_map(start=self._start_node, end=valve_name, is_symmetric=False)

        for start, end in combinations(self._non_broken_valves, 2):
            self._set_valve_map(start=start, end=end, is_symmetric=True)

    def _set_valve_map(self, start: str, end: str, is_symmetric: bool = True):
        _path = find_path(self._simple_graph, start, end)
        if _path.total_cost <= self._max_time:
            self._valve_map[start].add((_path.total_cost, self._valves[end].flow_rate, end))
            if is_symmetric:
                self._valve_map[end].add((_path.total_cost, self._valves[start].flow_rate, start))

    def get_max_flow(self) -> int:
        queue = []
        if self._start_node not in self._non_broken_valves:
            heappush(queue, (0, 0, [self._start_node]))
        else:
            for (time_delta, flow_rate, next_valve_name) in self._valve_map[self._start_node]:
                _flow = flow_rate * (self._max_time - time_delta)
                heappush(queue, (time_delta, _flow, [next_valve_name]))

            _flow = self._valves[self._start_node].flow_rate * (self._max_time - 1)
            heappush(queue, (1, _flow, [self._start_node]))

        queue_collection = [queue]

        max_flow = 0

        while queue_collection:
            current_queue = queue_collection.pop(0)
            new_queue = []
            while current_queue:
                path_flow, path_time, path_nodes = heappop(current_queue)

                if path_flow < max_flow:
                    max_flow = path_flow

                if not self._non_broken_valves - set(path_nodes):
                    return -path_flow

                next_paths = self._get_next_paths(
                    current_flow=path_flow, current_time=path_time, current_nodes=path_nodes
                )

                for path in next_paths:
                    heappush(new_queue, path)

            if new_queue:
                queue_collection.append(new_queue)

        return -max_flow

    def _get_next_paths(
            self, current_flow: int, current_time: int, current_nodes: List[str]) -> List[Tuple[int, int, List[str]]]:
        possible_next_nodes = [_ for _ in self._valve_map[current_nodes[-1]] if _[2] not in current_nodes]

        next_paths = []
        for time_delta, flow_rate, next_valve in possible_next_nodes:
            if (next_time := current_time + time_delta + 1) >= self._max_time:
                continue

            next_nodes = current_nodes + [next_valve]
            next_flow = current_flow + (flow_rate * (self._max_time - current_time - time_delta - 1))

            next_paths.append((next_flow, next_time, next_nodes))

        return next_paths

    def get_max_flow_with_elephant_support(self):
        pass
