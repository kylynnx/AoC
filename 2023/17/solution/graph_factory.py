from typing import Tuple

from dijkstar import Graph

from heat_loss_map import HeatLossMap
from base_definitions import Direction, rotate_direction


class GraphFactory:

    def __init__(self, min_steps: int, max_steps: int):
        self._min_steps = min_steps
        self._max_steps = max_steps

    def get_graph(self, heat_loss_map: HeatLossMap) -> Graph:
        graph = Graph(undirected=False)
        for index_x in range(0, heat_loss_map.dim_x):
            for index_y in range(0, heat_loss_map.dim_y):
                if index_x == 0 and index_y == 0:
                    self._set_start_edges(heat_loss_map=heat_loss_map, graph=graph)
                elif index_x == heat_loss_map.dim_x - 1 and index_y == heat_loss_map.dim_y - 1:
                    break
                else:
                    self._set_internal_edges(heat_loss_map=heat_loss_map, graph=graph, point=(index_x, index_y))
        return graph

    @staticmethod
    def _move_in_direction(count_moves: int, direction: Direction, point: Tuple[int, int]) -> Tuple[int, int]:
        _new_x = point[0] + (count_moves * direction.value[0])
        _new_y = point[1] + (count_moves * direction.value[1])

        return _new_x, _new_y

    def _set_start_edges(self, heat_loss_map: HeatLossMap, graph: Graph):
        start = (0, 0)
        for direction in [Direction.RIGHT, Direction.DOWN]:
            _moves_in_direction = 1
            _heat_loss = 0
            can_move = True
            while _moves_in_direction < self._min_steps:
                _new_x, _new_y = self._move_in_direction(
                    count_moves=_moves_in_direction, direction=direction, point=start
                )
                if (_new_x, _new_y) not in heat_loss_map:
                    can_move = False
                    break
                _heat_loss += heat_loss_map.get_heat_loss((_new_x, _new_y))
                _moves_in_direction += 1

            while _moves_in_direction <= self._max_steps and can_move:
                _new_x, _new_y = self._move_in_direction(
                    count_moves=_moves_in_direction, direction=direction, point=start
                )
                if (_new_x, _new_y) not in heat_loss_map:
                    break
                _heat_loss += heat_loss_map.get_heat_loss((_new_x, _new_y))
                graph.add_edge(start, (_new_x, _new_y, _moves_in_direction, direction.value[2]), _heat_loss)
                _moves_in_direction += 1

    def _set_internal_edges(self, point: Tuple[int, int], heat_loss_map: HeatLossMap, graph: Graph):
        for direction in list(Direction):
            _moves_in_direction = self._min_steps

            while _moves_in_direction <= self._max_steps:
                self._set_internal_edges_same_direction(
                    point=point, heat_loss_map=heat_loss_map, graph=graph, previous_moves=_moves_in_direction,
                    direction=direction
                )
                self._set_internal_edges_different_direction(
                    point=point, heat_loss_map=heat_loss_map, graph=graph, previous_moves=_moves_in_direction,
                    direction=direction
                )
                _moves_in_direction += 1

    def _set_internal_edges_same_direction(
            self, point: Tuple[int, int], heat_loss_map: HeatLossMap, graph: Graph, direction: Direction,
            previous_moves: int
    ):
        heat_loss = 0
        can_move = True
        for count_next_moves in range(0, previous_moves):
            _new_x, _new_y = self._move_in_direction(
                count_moves=count_next_moves, direction=direction, point=point
            )

            if (_new_x, _new_y) not in heat_loss_map:
                can_move = False
                break

            heat_loss += heat_loss_map.get_heat_loss((_new_x, _new_y))

        if can_move:
            for count_next_moves in range(1, self._max_steps - previous_moves + 1):
                _new_x, _new_y = self._move_in_direction(count_moves=count_next_moves, direction=direction, point=point)
                next_coordinate = (_new_x, _new_y)

                if next_coordinate not in heat_loss_map:
                    break

                heat_loss += heat_loss_map.get_heat_loss(next_coordinate)

                if _new_x == heat_loss_map.dim_x - 1 and _new_y == heat_loss_map.dim_y - 1:
                    graph.add_edge(
                        (point[0], point[1], previous_moves, direction.value[2]),
                        (_new_x, _new_y),
                        heat_loss
                    )
                    break

                graph.add_edge(
                    (point[0], point[1], previous_moves, direction.value[2]),
                    (_new_x, _new_y, previous_moves + count_next_moves, direction.value[2]),
                    heat_loss
                )

    def _set_internal_edges_different_direction(
            self, point: Tuple[int, int], heat_loss_map: HeatLossMap, graph: Graph, direction: Direction,
            previous_moves: int
    ):
        for new_direction in rotate_direction(direction=direction):
            heat_loss = 0
            _moves_in_direction = 1
            can_move = True
            while _moves_in_direction < self._min_steps:
                _new_x, _new_y = self._move_in_direction(
                    count_moves=_moves_in_direction, direction=new_direction, point=point
                )
                if (_new_x, _new_y) not in heat_loss_map:
                    can_move = False
                    break
                heat_loss += heat_loss_map.get_heat_loss((_new_x, _new_y))
                _moves_in_direction += 1

            while _moves_in_direction <= self._max_steps and can_move:
                _new_x, _new_y = self._move_in_direction(
                    count_moves=_moves_in_direction, direction=new_direction, point=point
                )
                next_coordinate = (_new_x, _new_y)

                if next_coordinate not in heat_loss_map:
                    break

                heat_loss += heat_loss_map.get_heat_loss(next_coordinate)

                if _new_x == heat_loss_map.dim_x - 1 and _new_y == heat_loss_map.dim_y - 1:
                    graph.add_edge(
                        (point[0], point[1], previous_moves, direction.value[2]),
                        (_new_x, _new_y),
                        heat_loss
                    )
                    break

                graph.add_edge(
                    (point[0], point[1], previous_moves, direction.value[2]),
                    (_new_x, _new_y, _moves_in_direction, new_direction.value[2]),
                    heat_loss
                )

                _moves_in_direction += 1
