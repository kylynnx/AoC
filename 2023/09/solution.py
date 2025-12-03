from typing import List


class History:
    def __init__(self, history_string: str):
        self._start_history = [int(_) for _ in history_string.split(' ')]
        self._extrapolation = None
        self._reverse_extrapolation = None

    @property
    def extrapolation(self):
        if self._extrapolation is None:
            self._extrapolation = History._extrapolate(self._start_history)

        return self._extrapolation

    @property
    def reverse_extrapolation(self):
        if self._reverse_extrapolation is None:
            self._reverse_extrapolation = History._extrapolate(self._start_history, reverse=True)

        return self._reverse_extrapolation

    @staticmethod
    def _extrapolate(start_history: List[int], reverse: bool = False):
        _extrapolated = [[_ for _ in start_history]]

        if reverse:
            _extrapolated[0].reverse()

        _next_line = [1]

        while any(_next_line):
            _previous_line = _extrapolated[-1]
            _next_line = [_ - __ for _, __ in zip(_previous_line[1:], _previous_line[:-1])]
            _extrapolated.append(_next_line)

        _extrapolated[-1].append(0)

        for line in range(len(_extrapolated) - 1):
            _lookup_index = - line - 1
            _add_index = _lookup_index - 1
            _extrapolated[_add_index].append(_extrapolated[_add_index][-1] + _extrapolated[_lookup_index][-1])

        return _extrapolated[0][-1]


class OASIS:
    def __init__(self, filename: str):
        with open(filename, 'r') as _f:
            histories = _f.readlines()
        self._histories = [History(_) for _ in histories]
        self._extrapolation = None
        self._reverse_extrapolation = None

    @property
    def extrapolation(self):
        if self._extrapolation is None:
            result = 0
            for history in self._histories:
                result += history.extrapolation
            self._extrapolation = result
        return self._extrapolation

    @property
    def reverse_extrapolation(self):
        if self._reverse_extrapolation is None:
            result = 0
            for history in self._histories:
                result += history.reverse_extrapolation
            self._reverse_extrapolation = result
        return self._reverse_extrapolation


def main(filename: str):
    oasis = OASIS(filename)
    print(oasis.extrapolation)
    print(oasis.reverse_extrapolation)


if __name__ == '__main__':
    main('./input.txt')
