import re
from typing import Dict, List, Optional

from pulse import Pulse, PulseType
from pulse_count import PulseCount
from pulse_modules import ModuleType, PulseModule, Broadcaster, OutputModule


class ControlPanel:
    def __init__(self, filename: Optional[str] = None, pulse_modules: Optional[Dict[str, PulseModule]] = None):
        if filename is not None:
            self._pulse_modules = self._get_pulse_modules(filename)
        elif pulse_modules is not None:
            self._pulse_modules = pulse_modules
        else:
            raise ValueError('Must either provide `filename` or `pulse_modules`')
        self._pulse_counts: List[PulseCount] = []

    @property
    def is_in_start_position(self):
        return all(_.is_in_start_position for _ in self._pulse_modules.values())

    @staticmethod
    def _get_pulse_modules(filename: str) -> Dict[str, PulseModule]:
        target_map = {}
        target_set = set()
        source_map = {}
        klass_map = {}
        names = set()
        modules = {}
        with open(filename, 'r') as _f:
            raw_lines = _f.readlines()

        for line in raw_lines:
            identifier, target_list = line.split(' -> ')
            targets = target_list.strip('\n').split(', ')

            if identifier == 'broadcaster':
                modules[identifier] = Broadcaster(targets=targets)
                name = identifier
            else:
                match = re.match(r'([%&])([a-z]+)', identifier)
                kls = PulseModule.get_module_class(ModuleType(match.group(1)))
                name = match.group(2)
                names.add(name)
                klass_map[name] = kls
                target_map[name] = targets

                if name not in source_map:
                    source_map[name] = []

            for target in targets:
                target_set.add(target)
                if target in source_map:
                    source_map[target].append(name)
                else:
                    source_map[target] = [name]

        for name in names:
            modules[name] = klass_map[name](name=name, sources=source_map[name], targets=target_map[name])

        if outputs := (target_set - names):
            for output in outputs:
                modules[output] = OutputModule(name=output, sources=source_map[output])

        return modules

    def reset(self):
        self._pulse_counts = []
        for pulse_module in self._pulse_modules.values():
            pulse_module.reset()

    def get_module(self, module_name: str):
        return self._pulse_modules[module_name]

    def cycle(self):
        broadcaster = self._pulse_modules[ModuleType.BROADCASTER.value]

        pulses = broadcaster.handle_pulse(
            Pulse(pulse_type=PulseType.LOW, source='button', target=ModuleType.BROADCASTER.value)
        )
        pulse_count = PulseCount(low=1, high=0)

        while pulses:
            handled_pulse = pulses.pop(0)
            pulse_count.add_pulse(handled_pulse)
            pulses += self._pulse_modules[handled_pulse.target].handle_pulse(pulse=handled_pulse)

        self._pulse_counts.append(pulse_count)

    def warm_up(self, button_presses: int) -> int:
        self.cycle()
        _cycles = 1

        while not self.is_in_start_position and _cycles < button_presses:
            self.cycle()
            _cycles += 1

        _cycle_count = len(self._pulse_counts)

        count_all_cycles = button_presses // _cycle_count

        low_pulses = count_all_cycles * sum(_.low_pulses for _ in self._pulse_counts)
        high_pulses = count_all_cycles * sum(_.high_pulses for _ in self._pulse_counts)

        for additional_cycle in range(button_presses % _cycle_count):
            low_pulses += self._pulse_counts[additional_cycle].low_pulses
            high_pulses += self._pulse_counts[additional_cycle].high_pulses

        return low_pulses * high_pulses

    def get_button_presses_until_pulse(self, pulse_type: PulseType, module_name: str):
        self.reset()
        pulse_sent = False
        broadcaster = self._pulse_modules[ModuleType.BROADCASTER.value]

        button_presses = 0
        while not pulse_sent:
            button_presses += 1

            pulses = broadcaster.handle_pulse(
                Pulse(pulse_type=PulseType.LOW, source='button', target=ModuleType.BROADCASTER.value)
            )

            while pulses:
                handled_pulse = pulses.pop(0)
                if handled_pulse.pulse_type is pulse_type and handled_pulse.target == module_name:
                    pulse_sent = True
                    break
                pulses += self._pulse_modules[handled_pulse.target].handle_pulse(pulse=handled_pulse)
        return button_presses
