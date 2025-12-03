from pulse import Pulse, PulseType


class PulseCount:
    def __init__(self, low: int, high: int):
        self._high_pulses = high
        self._low_pulses = low

    @property
    def high_pulses(self):
        return self._high_pulses

    @property
    def low_pulses(self):
        return self._low_pulses

    def add_pulse(self, pulse: Pulse):
        if pulse.pulse_type is PulseType.HIGH:
            self._high_pulses += 1
        else:
            self._low_pulses += 1
