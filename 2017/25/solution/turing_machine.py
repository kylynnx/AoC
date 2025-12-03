from collections import defaultdict

from state import State


class TuringMachine:
    def __init__(self):
        self.state_map: dict[str, State] = {}
        self.tape = defaultdict(int)
        self.cursor = 0

    @property
    def checksum(self):
        return sum(self.tape.values())

    def register_state(self, state: State):
        self.state_map[state.name] = state

    def run(self, starting_state: str, steps: int):
        step = 0

        current_state = starting_state

        while step < steps:
            current_state, new_value, cursor_direction = self.state_map[current_state].evaluate(self.tape[self.cursor])
            self.tape[self.cursor] = new_value
            self.cursor += cursor_direction
            step += 1
