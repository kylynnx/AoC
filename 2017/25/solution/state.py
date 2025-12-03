class State:
    def __init__(self, name: str, value_map: dict[int, int], state_map: dict[int, str], direction_map: dict[int, int]):
        self.name = name
        self.value_map = value_map
        self.state_map = state_map
        self.direction_map = direction_map

    def evaluate(self, value: int) -> tuple[str, int, int]:
        return self.state_map[value], self.value_map[value], self.direction_map[value]
