import re

from state import State


class StateFactory:
    @staticmethod
    def load(filename: str) -> tuple[list[State], str, int]:
        with open(filename) as f:
            description = f.read()

        metadata, *state_descriptions = description.strip().split("\n\n")

        starting_state, steps = StateFactory.load_metadata(metadata)

        states = [StateFactory.load_state(_) for _ in state_descriptions]

        return states, starting_state, steps

    @staticmethod
    def load_metadata(metadata: str) -> tuple[str, int]:
        starting_state_description, steps_description = metadata.split("\n")

        return (
            StateFactory.load_starting_state(starting_state_description),
            StateFactory.load_steps(steps_description),
        )

    @staticmethod
    def load_starting_state(description: str) -> str:
        re_match = re.match(r"^Begin in state ([A-Z]).$", description)

        return re_match.group(1)

    @staticmethod
    def load_steps(description: str) -> int:
        re_match = re.match(r"^Perform a diagnostic checksum after ([1-9]+) steps.$", description)

        return int(re_match.group(1))

    @staticmethod
    def load_state(description: str) -> State:
        name_description, *mappings  = description.split("If")

        name = StateFactory.load_name(name_description)

        value_map = {}
        state_map = {}
        direction_map = {}

        for idx, mapping in enumerate(mappings):
            value, state, direction = StateFactory.load_mapping(mapping)
            value_map[idx] = value
            state_map[idx] = state
            direction_map[idx] = direction

        return State(name=name, value_map=value_map, state_map=state_map, direction_map=direction_map)

    @staticmethod
    def load_name(description: str) -> str:
        re_match = re.match(r"In state ([A-Z])", description)

        return re_match.group(1)

    @staticmethod
    def load_mapping(mapping: str) -> tuple[int, str, int]:
        _, value_description, direction_description, state_description = mapping.strip().split("\n")

        value = StateFactory.load_value_mapping(value_description)
        state = StateFactory.load_state_mapping(state_description)
        direction = StateFactory.load_direction_mapping(direction_description)

        return value, state, direction

    @staticmethod
    def load_value_mapping(description: str) -> int:
        re_match = re.search(r"Write the value ([0-9]).", description)

        return int(re_match.group(1))

    @staticmethod
    def load_state_mapping(description: str) -> str:
        re_match = re.search(r"Continue with state ([A-Z])", description)

        return re_match.group(1)

    @staticmethod
    def load_direction_mapping(description: str) -> int:
        re_match = re.search(r"Move one slot to the (left|right)", description)

        return 1 if re_match.group(1) == "right" else -1
