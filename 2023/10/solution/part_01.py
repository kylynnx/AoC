import math
from typing import List

from definitions import Coordinate, Maze, Start


class DistanceMaze(Maze):
    def __init__(self, filename: str):
        super().__init__(filename=filename)
        self._is_part_map: List[bool] = []
        self._circumference = None

    @property
    def part_map(self):
        if not self._is_part_map:
            self._set_parts()

        return self._is_part_map

    @property
    def circumference(self):
        if self._circumference is None:
            self._circumference = sum(self.part_map)

        return self._circumference

    @property
    def max_distance(self):
        if not self._max_distance:
            self._max_distance = math.ceil(self.circumference / 2)

        return self._max_distance

    def _set_is_part_at(self, coordinate: Coordinate):
        lexic_coordinate = self.to_lexic(coordinate)

        self._is_part_map[lexic_coordinate] = True

    def _set_parts(self):
        self._is_part_map = [False] * self._max_lexic

        start = self._get(self._starting_position)
        if start is not Start:
            raise ValueError('Start not identified correctly.')

        self._set_is_part_at(self._starting_position)
        start_moves = self._get_start_moves()

        move = start_moves[0]
        self._set_is_part_at(move.coordinate)
        current_position = self._get(move.coordinate)
        while current_position != start:
            move = move + current_position.lookup(move.cardinal)
            self._set_is_part_at(move.coordinate)
            current_position = self._get(move.coordinate)


def main(filename: str):
    maze = DistanceMaze(filename)
    print(maze.max_distance)


if __name__ == '__main__':
    main('../input.txt')
