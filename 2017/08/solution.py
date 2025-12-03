import re
from collections import defaultdict


class Machine:
    def __init__(self):
        self._registers = defaultdict(int)
        self._max_value_overall = 0

    @property
    def max_register_value(self):
        return max(self._registers.values())

    @property
    def max_value_overall(self):
        return self._max_value_overall

    def handle_instruction(self, instruction: str):
        match = re.match(r"^([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) ([!><=]+) (-?\d+)$", instruction)
        target_register = match.group(1)
        operation = match.group(2)
        value = int(match.group(3))
        comparison_register = match.group(4)
        comparison_operator = match.group(5)
        comparison_value = int(match.group(6))

        if self._compare(register=comparison_register, operator=comparison_operator, value=comparison_value):
            self._execute(register=target_register, operation=operation, value=value)
            self._max_value_overall = max(max(self._registers.values()), self._max_value_overall)

    def _compare(self, register: str, operator: str, value: int) -> bool:
        match operator:
            case "<":
                return self._registers[register] < value
            case "<=":
                return self._registers[register] <= value
            case "==":
                return self._registers[register] == value
            case ">=":
                return self._registers[register] >= value
            case ">":
                return self._registers[register] > value

        return self._registers[register] != value

    def _execute(self, register: str, operation: str, value: int):
        if operation == "inc":
            self._registers[register] += value
        else:
            self._registers[register] -= value


def main(filename: str):
    with open(filename) as f:
        instructions = [_.strip() for _ in f.readlines()]

    machine = Machine()
    for instruction in instructions:
        machine.handle_instruction(instruction)

    print(f"After all instructions are executed, the largest register value is {machine.max_register_value}.")
    print(f"The largest register value during the entire program is {machine.max_value_overall}.")


if __name__ == "__main__":
    main("input.txt")
