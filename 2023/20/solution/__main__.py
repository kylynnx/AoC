import math

from control_panel import ControlPanel
from pulse import PulseType


def part_one(filename: str):
    control_panel = ControlPanel(filename)
    pulse_product = control_panel.warm_up(1000)
    print(pulse_product)


def part_two(filename: str):
    control_panel = ControlPanel(filename)
    target_module = control_panel.get_module('rx')
    conjunction = control_panel.get_module(target_module.sources[0])
    conjunction_inputs = conjunction.sources

    button_presses = []
    for source in conjunction_inputs:
        button_presses.append(
            control_panel.get_button_presses_until_pulse(pulse_type=PulseType.LOW, module_name=source)
        )
    print(math.lcm(*button_presses))


def main(filename: str):
    part_one(filename)
    part_two(filename)


if __name__ == '__main__':
    main('../input.txt')
