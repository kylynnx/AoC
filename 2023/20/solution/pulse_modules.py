from abc import abstractmethod
from enum import Enum
from typing import List, Dict, Type

from pulse import Pulse, PulseType


class ModuleType(Enum):
    FLIP_FLOP = '%'
    CONJUNCTION = '&'
    BROADCASTER = 'broadcaster'
    OUTPUT = 'output'


class FlipFlopState(Enum):
    ON = True
    OFF = False


class PulseModule:
    _module_type: ModuleType = None
    __known_modules: Dict[ModuleType, Type['PulseModule']] = {}

    def __init_subclass__(cls, **kwargs):
        if cls._module_type is None:
            raise ValueError('Must set `module_type`')

        PulseModule.__known_modules[cls._module_type] = cls

    def __init__(self, name: str, sources: List[str], targets: List[str]):
        self._name = name
        self._sources = sources
        self._targets = targets

    @property
    def name(self):
        return self._name

    @property
    def sources(self):
        return self._sources

    @property
    def targets(self):
        return self._targets

    @abstractmethod
    def handle_pulse(self, pulse: Pulse) -> List[Pulse]:
        pass

    @property
    @abstractmethod
    def is_in_start_position(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @staticmethod
    def get_module_class(module_type: ModuleType) -> Type['PulseModule']:
        return PulseModule.__known_modules[module_type]


class FlipFlop(PulseModule):
    _module_type = ModuleType.FLIP_FLOP

    def __init__(self, name: str, sources: List[str], targets: List[str]):
        super().__init__(name=name, sources=sources, targets=targets)
        self._state = FlipFlopState.OFF

    def handle_pulse(self, pulse: Pulse) -> List[Pulse]:
        if pulse.pulse_type is PulseType.HIGH:
            return []

        if self._state is FlipFlopState.ON:
            _pulses = [Pulse(source=self._name, target=_, pulse_type=PulseType.LOW) for _ in self._targets]
            self._state = FlipFlopState.OFF
        else:
            _pulses = [Pulse(source=self._name, target=_, pulse_type=PulseType.HIGH) for _ in self._targets]
            self._state = FlipFlopState.ON

        return _pulses

    @property
    def is_in_start_position(self):
        return not self._state.value

    def reset(self):
        self._state = FlipFlopState.OFF


class Conjunction(PulseModule):
    _module_type = ModuleType.CONJUNCTION

    def __init__(self, name: str, sources: List[str], targets: List[str]):
        super().__init__(name=name, sources=sources, targets=targets)
        self._remembered_pulses = {_: PulseType.LOW for _ in sources}
        self._source_count = len(sources)

    def handle_pulse(self, pulse: Pulse) -> List[Pulse]:
        self._remembered_pulses[pulse.source] = pulse.pulse_type

        if sum(_.value for _ in self._remembered_pulses.values()) == self._source_count:
            _pulses = [Pulse(source=self._name, target=_, pulse_type=PulseType.LOW) for _ in self._targets]
        else:
            _pulses = [Pulse(source=self._name, target=_, pulse_type=PulseType.HIGH) for _ in self._targets]

        return _pulses

    @property
    def is_in_start_position(self):
        return sum(_.value for _ in self._remembered_pulses.values()) == 0

    def reset(self):
        self._remembered_pulses = {_: PulseType.LOW for _ in self._sources}


class Broadcaster(PulseModule):
    _module_type = ModuleType.BROADCASTER

    def __init__(self, targets: List[str]):
        super().__init__(name='broadcaster', sources=[], targets=targets)

    def handle_pulse(self, pulse: Pulse) -> List[Pulse]:
        return [Pulse(source=self._name, target=_, pulse_type=pulse.pulse_type) for _ in self._targets]

    @property
    def is_in_start_position(self):
        return True

    def reset(self):
        pass


class OutputModule(PulseModule):
    _module_type = ModuleType.OUTPUT

    def __init__(self, name: str, sources: List[str]):
        super().__init__(name=name, sources=sources, targets=[])

    def handle_pulse(self, pulse: Pulse) -> List[Pulse]:
        return []

    @property
    def is_in_start_position(self):
        return True

    def reset(self):
        pass
