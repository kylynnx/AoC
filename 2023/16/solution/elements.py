from enum import Enum
from typing import Dict, List, Tuple, Type


class Directions(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'


class ElementType(Enum):
    EMPTY = '.'
    HORIZONTAL_SPLITTER = '|'
    VERTICAL_SPLITTER = '-'
    LEFT_MIRROR = '\\'
    RIGHT_MIRROR = '/'
    BEAM_STOPPER = '*'
    ENERGIZED = '#'


class Coordinate:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class ElementFactory:
    __registered_elements: Dict[ElementType, Type['LightElement']] = {}

    @staticmethod
    def register(element_type: ElementType, element_class: Type['LightElement']):
        ElementFactory.__registered_elements[element_type] = element_class

    @staticmethod
    def get_element(element_str: str, coordinate: Coordinate):
        return ElementFactory.__registered_elements[ElementType(element_str)](coordinate)


class LightElement:
    _element_type: ElementType = None
    _direction_mapping: Dict[Directions, Tuple[Directions, ...]] = {}

    def __init_subclass__(cls, **kwargs):
        if cls._element_type is None:
            raise ValueError('Must set `element_type`')

        ElementFactory.register(element_type=cls._element_type, element_class=cls)

    def __init__(self, coordinate: Coordinate):
        self._is_energized = False
        self._entry_directions = set()
        self._coordinate = coordinate

    @property
    def is_energized(self):
        return self._is_energized

    def __str__(self):
        return self._element_type.value

    @property
    def energy_string(self):
        if self._is_energized:
            return ElementType.ENERGIZED.value

        return ElementType.EMPTY.value

    def _energize(self):
        self._is_energized = True

    def reset(self):
        self._is_energized = False
        self._entry_directions = set()

    def propagate(self, entry_direction: Directions) -> List[Tuple[Directions, Coordinate]]:
        if entry_direction in self._entry_directions:
            return []

        self._entry_directions.add(entry_direction)

        self._energize()

        if entry_direction in self._direction_mapping:
            return [(_, self._move_in_direction(_)) for _ in self._direction_mapping[entry_direction]]

        return [(entry_direction, self._move_in_direction(entry_direction))]

    def _move_in_direction(self, exit_direction: Directions) -> Coordinate:
        match exit_direction:
            case Directions.UP:
                return Coordinate(x=self._coordinate.x, y=self._coordinate.y - 1)
            case Directions.DOWN:
                return Coordinate(x=self._coordinate.x, y=self._coordinate.y + 1)
            case Directions.LEFT:
                return Coordinate(x=self._coordinate.x - 1, y=self._coordinate.y)
            case Directions.RIGHT:
                return Coordinate(x=self._coordinate.x + 1, y=self._coordinate.y)


class BeamStopper(LightElement):
    _element_type = ElementType.BEAM_STOPPER

    def propagate(self, entry_direction: Directions) -> List[Coordinate]:
        return []

    @property
    def energy_string(self):
        return ElementType.BEAM_STOPPER.value


class HorizontalSplitter(LightElement):
    _element_type = ElementType.HORIZONTAL_SPLITTER
    _direction_mapping = {
        Directions.RIGHT: (Directions.UP, Directions.DOWN),
        Directions.LEFT: (Directions.UP, Directions.DOWN)
    }


class VerticalSplitter(LightElement):
    _element_type = ElementType.VERTICAL_SPLITTER
    _direction_mapping = {
        Directions.UP: (Directions.LEFT, Directions.RIGHT),
        Directions.DOWN: (Directions.LEFT, Directions.RIGHT)
    }


class RightMirror(LightElement):
    _element_type = ElementType.RIGHT_MIRROR
    _direction_mapping = {
        Directions.LEFT: (Directions.DOWN,),
        Directions.RIGHT: (Directions.UP,),
        Directions.UP: (Directions.RIGHT,),
        Directions.DOWN: (Directions.LEFT,)
    }


class LeftMirror(LightElement):
    _element_type = ElementType.LEFT_MIRROR
    _direction_mapping = {
        Directions.LEFT: (Directions.UP,),
        Directions.RIGHT: (Directions.DOWN,),
        Directions.UP: (Directions.LEFT,),
        Directions.DOWN: (Directions.RIGHT,)
    }


class Empty(LightElement):
    _element_type = ElementType.EMPTY
