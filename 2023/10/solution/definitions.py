from enum import Enum
from typing import Dict, Tuple, Type, Union, List

MAZE_TYPE = Union[Type['Pipe'], Type['Start'], Type['Ground']]


class Cardinal(Enum):
    NORTH = 'north'
    EAST = 'east'
    SOUTH = 'south'
    WEST = 'west'


class Ground:
    @classmethod
    def contains(cls, _item):
        return False


class Start:
    pass


class Coordinate:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __add__(self, other: 'Coordinate'):
        return Coordinate(x=self._x + other.x, y=self._y + other.y)


go_north = Coordinate(x=0, y=-1)
go_east = Coordinate(x=1, y=0)
go_south = Coordinate(x=0, y=1)
go_west = Coordinate(x=-1, y=0)


class Move:
    def __init__(self, coordinate: Coordinate, cardinal: Cardinal):
        self._cardinal = cardinal
        self._coordinate = coordinate

    @property
    def cardinal(self):
        return self._cardinal

    @property
    def coordinate(self):
        return self._coordinate

    def __add__(self, other: 'Move'):
        # attention: Non-commutative
        return Move(
            coordinate=self.coordinate + other.coordinate,
            cardinal=other.cardinal
        )


class Pipe:
    _connection_lookup: Dict[Cardinal, Tuple[int, int]] = None

    def __init_subclass__(cls, **kwargs):
        if not cls._connection_lookup:
            raise ValueError('Must set `_connection_lookup`')

    @classmethod
    def contains(cls, item: Coordinate):
        return item in cls._connection_lookup

    @classmethod
    def lookup(cls, cardinal: Cardinal):
        return cls._connection_lookup[cardinal]


class VerticalPipe(Pipe):
    _connection_lookup = {
        Cardinal.NORTH: Move(coordinate=go_south, cardinal=Cardinal.NORTH),
        Cardinal.SOUTH: Move(coordinate=go_north, cardinal=Cardinal.SOUTH)
    }


class HorizontalPipe(Pipe):
    _connection_lookup = {
        Cardinal.WEST: Move(coordinate=go_east, cardinal=Cardinal.WEST),
        Cardinal.EAST: Move(coordinate=go_west, cardinal=Cardinal.EAST)
    }


class LPipe(Pipe):
    _connection_lookup = {
        Cardinal.NORTH: Move(coordinate=go_east, cardinal=Cardinal.WEST),
        Cardinal.EAST: Move(coordinate=go_north, cardinal=Cardinal.SOUTH)
    }


class JPipe(Pipe):
    _connection_lookup = {
        Cardinal.WEST: Move(coordinate=go_north, cardinal=Cardinal.SOUTH),
        Cardinal.NORTH: Move(coordinate=go_west, cardinal=Cardinal.EAST)
    }


class SevenPipe(Pipe):
    _connection_lookup = {
        Cardinal.WEST: Move(coordinate=go_south, cardinal=Cardinal.NORTH),
        Cardinal.SOUTH: Move(coordinate=go_west, cardinal=Cardinal.EAST)
    }


class FPipe(Pipe):
    _connection_lookup = {
        Cardinal.SOUTH: Move(coordinate=go_east, cardinal=Cardinal.WEST),
        Cardinal.EAST: Move(coordinate=go_south, cardinal=Cardinal.NORTH)
    }


class PipeFactory:
    @staticmethod
    def produce(pipe_string: str) -> MAZE_TYPE:
        match pipe_string:
            case '|':
                return VerticalPipe
            case '-':
                return HorizontalPipe
            case 'L':
                return LPipe
            case 'J':
                return JPipe
            case '7':
                return SevenPipe
            case 'F':
                return FPipe
            case 'S':
                return Start
            case _:
                return Ground


STARTING_NAME = 'S'


class Maze:
    def __init__(self, filename: str):
        self._maze = []
        with open(filename, 'r') as _f:
            pipe_rows = _f.readlines()

        self._starting_position = (None, None)
        self._max_distance = None

        for pipe_row in pipe_rows:
            pipe_row.strip('\n')
            self._maze += [PipeFactory.produce(_) for _ in pipe_row]

            if STARTING_NAME in pipe_row:
                self._x_dim = len(pipe_row)
                self._starting_position = Coordinate(*self.to_cartesian(self._maze.index(Start)))

        self._max_lexic = len(self._maze)

    def to_cartesian(self, lexic_index: int) -> Tuple[int, int]:
        return lexic_index % self._x_dim, lexic_index // self._x_dim

    def to_lexic(self, coordinate: Coordinate) -> int:
        return (coordinate.y * self._x_dim) + coordinate.x

    def __contains__(self, item: Coordinate):
        return 0 <= self.to_lexic(item) < self._max_lexic

    def _get(self, coordinate: Coordinate) -> MAZE_TYPE:
        return self._maze[self.to_lexic(coordinate)]

    def _get_start_moves(self) -> List[Move]:
        _start_moves = []

        potential_moves = (
            (go_north, Cardinal.SOUTH), (go_east, Cardinal.WEST), (go_south, Cardinal.NORTH), (go_west, Cardinal.EAST)
        )
        for coordinate, cardinal in potential_moves:
            if (use_cord := self._starting_position + coordinate) in self:
                if self._get(use_cord).contains(cardinal):
                    _start_moves.append(Move(coordinate=use_cord, cardinal=cardinal))

        if len(_start_moves) > 2:
            raise ValueError('Too many start connections')

        return _start_moves

