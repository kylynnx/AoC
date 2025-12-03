from definitions import Cardinal
from part_01 import DistanceMaze


class AreaMaze(DistanceMaze):
    def __init__(self, filename: str):
        super().__init__(filename=filename)
        self._area = None
        self._internals = None

    @property
    def area(self):
        # https://en.wikipedia.org/wiki/Shoelace_formula
        if self._area is None:
            self._set_area()

        return self._area

    @property
    def internals(self):
        # https://en.wikipedia.org/wiki/Pick%27s_theorem
        if self._internals is None:
            self._internals = self.area - (self.circumference / 2) + 1

        return self._internals

    def _set_area(self):
        _area = 0

        start = self._get(self._starting_position)
        start_moves = self._get_start_moves()

        move = start_moves[0] if start_moves[0].cardinal in [Cardinal.EAST, Cardinal.SOUTH] else start_moves[1]
        current_coordinate = self._starting_position

        next_coordinate = move.coordinate
        _area += current_coordinate.x * next_coordinate.y
        _area -= current_coordinate.y * next_coordinate.x

        current_coordinate = next_coordinate
        current_position = self._get(move.coordinate)

        while current_position != start:
            move = move + current_position.lookup(move.cardinal)

            next_coordinate = move.coordinate
            _area += current_coordinate.x * next_coordinate.y
            _area -= current_coordinate.y * next_coordinate.x

            current_coordinate = next_coordinate
            current_position = self._get(move.coordinate)

        self._area = _area / 2


def main(filename: str):
    maze = AreaMaze(filename)
    print(maze.internals)


if __name__ == '__main__':
    main('../input.txt')
