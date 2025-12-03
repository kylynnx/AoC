from state_factory import StateFactory
from turing_machine import TuringMachine


def main(filename: str):
    states, starting_state, steps = StateFactory.load(filename)
    turing_machine = TuringMachine()

    for state in states:
        turing_machine.register_state(state)

    turing_machine.run(starting_state=starting_state, steps=steps)

    print(f"After {steps} steps the checksum is {turing_machine.checksum}")


if __name__ == "__main__":
    main("../test.txt")
    main("../input.txt")
