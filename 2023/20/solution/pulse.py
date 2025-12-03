from enum import Enum


class PulseType(Enum):
    LOW = 0
    HIGH = 1


class Pulse:
    def __init__(self, pulse_type: PulseType, source: str, target: str):
        self._pulse_type = pulse_type
        self._source = source
        self._target = target

    @property
    def pulse_type(self):
        return self._pulse_type

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    def __str__(self):
        return f'{self._source} -> {self._target}: {self._pulse_type.value}'
