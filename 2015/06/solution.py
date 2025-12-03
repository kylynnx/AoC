import re
from enum import Enum

coordinate_regex = r"([0-9]{1,3}),([0-9]{1,3}) through ([0-9]{1,3}),([0-9]{1,3})"


class Instruction(Enum):
    TURN_ON = "turn on"
    TURN_OFF = "turn off"
    TOGGLE = "toggle"


class Coordinate:
    def __init__(self, x, y):
        self._x = int(x)
        self._y = int(y)

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def lexic(self) -> int:
        return Coordinate.get_lexic(x=self._x, y=self._y)

    @staticmethod
    def get_lexic(x: int, y: int) -> int:
        return 1000 * y + x


class GridInstruction:
    def __init__(self):
        self._instruction = None
        self._start = None
        self._end = None

    @classmethod
    def from_string(cls, instruction_string: str) -> "GridInstruction":
        kls = cls()

        kls._get_instruction(instruction_string)
        kls._get_start_end(instruction_string)

        return kls

    @property
    def instruction(self) -> Instruction:
        return self._instruction

    def _get_instruction(self, instruction_string: str):
        if instruction_string.startswith(Instruction.TURN_ON.value):
            self._instruction = Instruction.TURN_ON
        elif instruction_string.startswith(Instruction.TURN_OFF.value):
            self._instruction = Instruction.TURN_OFF
        else:
            self._instruction = Instruction.TOGGLE

    def _get_start_end(self, instruction_string: str):
        match = re.search(coordinate_regex, instruction_string)
        self._start = Coordinate(x=match.group(1), y=match.group(2))
        self._end = Coordinate(x=match.group(3), y=match.group(4))

    def __iter__(self):
        for x in range(self._end.x - self._start.x + 1):
            for y in range(self._end.y - self._start.y + 1):
                yield Coordinate.get_lexic(x=self._start.x + x, y=self._start.y + y)


class LightGrid:
    def __init__(self, length: int = 1000, initial_value: int | bool = False):
        self._grid = [initial_value] * length * length

    def apply(self, grid_instruction: GridInstruction):
        match grid_instruction.instruction:
            case Instruction.TURN_ON:
                self._apply_on(grid_instruction)
            case Instruction.TURN_OFF:
                self._apply_off(grid_instruction)
            case _:
                self._apply_toggle(grid_instruction)

    def _apply_on(self, grid_instruction: GridInstruction):
        for field in grid_instruction:
            self._grid[field] = True

    def _apply_off(self, grid_instruction: GridInstruction):
        for field in grid_instruction:
            self._grid[field] = False

    def _apply_toggle(self, grid_instruction: GridInstruction):
        for field in grid_instruction:
            self._grid[field] = not self._grid[field]

    @property
    def lights(self):
        return sum(self._grid)


class OldElvishGrid(LightGrid):
    def __init__(self, length: int = 1000):
        super().__init__(length=length, initial_value=0)

    def _apply_on(self, grid_instruction: GridInstruction):
        for field in grid_instruction:
            self._grid[field] += 1

    def _apply_off(self, grid_instruction: GridInstruction):
        for field in grid_instruction:
            if self._grid[field] > 0:
                self._grid[field] -= 1

    def _apply_toggle(self, grid_instruction: GridInstruction):
        for field in grid_instruction:
            self._grid[field] += 2


def read_instructions(filename: str) -> list[GridInstruction]:
    with open(filename) as f:
        string_instructions = f.readlines()

    instructions = []

    for string_instruction in string_instructions:
        instructions.append(GridInstruction.from_string(string_instruction))

    return instructions


def main(filename: str):
    grid_one = LightGrid()
    grid_two = OldElvishGrid()
    instructions = read_instructions(filename)

    for instruction in instructions:
        grid_one.apply(instruction)
        grid_two.apply(instruction)

    print(grid_one.lights)
    print(grid_two.lights)


if __name__ == '__main__':
    main("input.txt")
