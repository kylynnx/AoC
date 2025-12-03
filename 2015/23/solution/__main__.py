from instruction import InstructionFactory
from machine import Machine


def main(filename: str):
    with open(filename) as f:
        instruction_strings = [_.strip("\n") for _ in f.readlines()]

    instructions = []
    for line in instruction_strings:
        instructions.append(InstructionFactory.produce(line))

    machine = Machine(instructions=instructions, start_registers={"a": 0, "b": 0})
    machine.run()
    print(machine.get_register("b"))

    machine = Machine(instructions=instructions, start_registers={"a": 1, "b": 0})
    machine.run()
    print(machine.get_register("b"))


if __name__ == '__main__':
    main("../input.txt")
