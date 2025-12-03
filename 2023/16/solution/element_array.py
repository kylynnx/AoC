from elements import Coordinate, Directions, ElementFactory


class ElementArray:
    def __init__(self, filename: str):
        with open(filename, 'r') as _f:
            element_lines = [_.strip('\n') for _ in _f.readlines()]
            element_lines = [f'*{_}*' for _ in element_lines]

        self._dim_x = len(element_lines[0])
        beam_stopper_string = '*' * self._dim_x
        element_lines.insert(0, beam_stopper_string)
        element_lines.append(beam_stopper_string)
        self._dim_y = len(element_lines)

        self._elements = []

        _current_y = 0
        for line in element_lines:
            _current_x = 0
            for element_str in line:
                self._elements.append(
                    ElementFactory.get_element(
                        element_str=element_str,
                        coordinate=Coordinate(x=_current_x, y=_current_y)
                    )
                )
                _current_x += 1
            _current_y += 1

        self._energy_sum = None

    def to_lexic(self, coordinate: Coordinate) -> int:
        return (self._dim_x * coordinate.y) + coordinate.x

    @property
    def dim_x(self):
        return self._dim_x

    @property
    def dim_y(self):
        return self._dim_y

    def __str__(self):
        _current_x = 1
        array_string = ''
        for element in self._elements:
            array_string += str(element)
            if _current_x and _current_x % self._dim_x == 0:
                array_string += '\n'
            _current_x += 1

        return array_string

    @property
    def energy_string(self):
        _current_x = 1
        array_string = ''
        for element in self._elements:
            array_string += element.energy_string
            if _current_x and _current_x % self._dim_x == 0:
                array_string += '\n'
            _current_x += 1

        return array_string

    def propagate_beam(self, entry_direction: Directions, entry_point: Coordinate):
        _stack = [(entry_direction, entry_point)]

        while _stack:
            direction, coordinate = _stack.pop(0)
            _stack += self._elements[self.to_lexic(coordinate)].propagate(direction)

    @property
    def energization(self):
        if self._energy_sum is None:
            self._energy_sum = sum(_.is_energized for _ in self._elements)

        return self._energy_sum

    def reset(self):
        self._energy_sum = None
        for element in self._elements:
            element.reset()
