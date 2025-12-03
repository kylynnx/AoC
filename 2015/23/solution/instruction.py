import re
from abc import abstractmethod


class Instruction:
    def __init__(self, register: str):
        self._register = register

    @property
    def register(self):
        return self._register

    @abstractmethod
    def process(self, value) -> tuple[int, int]:
        pass


class IncrementInstruction(Instruction):
    def process(self, value: int) -> tuple[int, int]:
        return value + 1, 1


class TripleInstruction(Instruction):
    def process(self, value: int) -> tuple[int, int]:
        return 3 * value, 1


class HalfInstruction(Instruction):
    def process(self, value: int) -> tuple[int, int]:
        return value // 2, 1


class JumpInstruction(Instruction):
    def __init__(self, register: str, offset: int):
        super().__init__(register=register)
        self._offset = offset

    def process(self, value: int) -> tuple[int, int]:
        return value, self._offset


class JumpIfEvenInstruction(JumpInstruction):
    def process(self, value: int) -> tuple[int, int]:
        if value % 2 == 0:
            return value, self._offset

        return value, 1


class JumpIfOneInstruction(JumpInstruction):
    def process(self, value: int) -> tuple[int, int]:
        if value == 1:
            return value, self._offset

        return value, 1


class InstructionFactory:
    @staticmethod
    def produce(instruction_string: str) -> Instruction:
        if instruction_string.startswith("j"):
            return InstructionFactory._produce_jump(instruction_string)

        instruction, register = instruction_string.split(" ")

        match instruction:
            case "inc":
                return IncrementInstruction(register=register)
            case "tpl":
                return TripleInstruction(register=register)

        return HalfInstruction(register=register)

    @staticmethod
    def _produce_jump(instruction_string: str) -> JumpInstruction:
        if "jmp" in instruction_string:
            _, offset = instruction_string.split(" ")
            return JumpInstruction(register="a", offset=int(offset))

        jump_match = re.match(r"(ji[eo]) ([ab]), (.+)", instruction_string)

        match jump_match.group(1):
            case "jio":
                return JumpIfOneInstruction(register=jump_match.group(2), offset=int(jump_match.group(3)))

            case "jie":
                return JumpIfEvenInstruction(register=jump_match.group(2), offset=int(jump_match.group(3)))
