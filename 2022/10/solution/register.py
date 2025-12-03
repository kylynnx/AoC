from typing import List


class Register:
    def __init__(self, initial_value: int = 1, break_points: List[int] = None):
        self._value = initial_value
        if break_points is None:
            self._break_points = [20, 60, 100, 140, 180, 220]
        else:
            self._break_points = break_points
        self._break_values = [0] * len(self._break_points)
        self._current_cycle = 1
        self._signal_strength = None
        self._break_point_index = 0
        self._break_point_count = len(self._break_points)
        self._crt = ''

    @property
    def crt(self):
        crt_image = ''

        for i in range(len(self._crt)):
            crt_image += self._crt[i]
            if i % 40 == 39:
                crt_image += '\n'

        return crt_image

    @property
    def signal_strength(self):
        if self._signal_strength is None:
            self._signal_strength = sum(_ * __ for _, __ in zip(self._break_points, self._break_values))

        return self._signal_strength

    def _update_crt(self, count_steps: int):
        for i in range(count_steps):
            cursor = (self._current_cycle + i - 1) % 40 + 1
            if self._value <= cursor < self._value + 3:
                self._crt += '#'
            else:
                self._crt += '.'

    def perform_operation(self, operation: str):
        if operation == "noop":
            value_change = 0
            cycle_change = 1
        else:
            value_change = int(operation.split(' ')[1])
            cycle_change = 2

        self._update_crt(cycle_change)
        self._current_cycle += cycle_change

        if (
            self._break_point_index is not None
            and self._current_cycle > self._break_points[self._break_point_index]
        ):
            self._break_values[self._break_point_index] = self._value
            if self._break_point_index < self._break_point_count - 1:
                self._break_point_index += 1
            else:
                self._break_point_index = None

        self._value += value_change
