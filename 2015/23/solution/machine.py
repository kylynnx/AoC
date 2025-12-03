import math

from instruction import Instruction


class Machine:
    def __init__(self, instructions: list[Instruction], start_registers: dict[str, int]):
        self._registers = start_registers
        self._instructions = instructions
        self._instruction_length = len(instructions)
        self._cursor = 0

    def run(self):
        while self._cursor < self._instruction_length:
            current_instruction = self._instructions[self._cursor]
            current_register = current_instruction.register
            new_register_value, cursor_delta = current_instruction.process(self._registers[current_register])

            self._registers[current_register] = new_register_value
            self._cursor += cursor_delta

            if self._registers["b"] == 1:
                return self._loop()

    def _loop(self):
        reg_a = self._registers["a"]
        log_a = math.log(reg_a, 2)
        reg_b = 1

        while log_a != int(log_a):
            reg_b += 1

            if reg_a % 2 == 0:
                reg_a //= 2
            else:
                reg_a *= 3
                reg_a += 1

            log_a = math.log(reg_a, 2)

        self._registers["b"] = reg_b + int(log_a) - 1

    def get_register(self, register: str) -> int:
        return self._registers[register]
