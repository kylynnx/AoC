import re


def main(filename: str):
    with open(filename) as f:
        program_strings = [_.strip("\n") for _ in f.readlines()]

    programs = load_programs(program_strings)
    bottom_program = find_bottom_program(programs)

    print(f"The name of the bottom program is {bottom_program}.")

    _, balance_weight = find_balance_weight(programs=programs, disc_program=bottom_program)
    print(f"The new weight to balance the tower is {balance_weight}.")


class Program:
    def __init__(self, name: str, weight: int, children: list[str]):
        self._name = name
        self._weight = weight
        self._children = children

    @property
    def name(self) -> str:
        return self._name

    @property
    def weight(self) -> int:
        return self._weight

    @property
    def children(self) -> list[str]:
        return self._children


def load_programs(program_strings: list) -> dict[str, Program]:
    programs = {}

    for program_string in program_strings:
        match = re.match(r"([a-z]+) \((\d+)\)", program_string)
        name = match.group(1)
        weight = int(match.group(2))

        if "->" in program_string:
            _, children_string = program_string.split(" -> ")
            children = children_string.split(", ")
        else:
            children = []

        programs[name] = Program(name=name, weight=weight, children=children)

    return programs


def find_bottom_program(programs: dict[str, Program]) -> str:
    top_programs = [_ for _, p in programs.items() if not p.children]
    parents = set([_ for _, p in programs.items() if any(n in p.children for n in top_programs)])

    while len(parents) > 1:
        parents = set([_ for _, p in programs.items() if any(n in p.children for n in parents)])

    return parents.pop()


def find_balance_weight(programs: dict[str, Program], disc_program: str, balance_weight: int | None = None) -> tuple[int, int | None]:
    expected_weight = None
    weight = programs[disc_program].weight

    expected_weight_child_name = ""
    children_with_bad_weight = []

    for child in programs[disc_program].children:
        child_weight, balance_weight = find_balance_weight(
            programs=programs, disc_program=child, balance_weight=balance_weight
        )
        weight += child_weight
        if expected_weight is None:
            expected_weight_child_name = child
            expected_weight = child_weight
        elif child_weight != expected_weight:
            children_with_bad_weight.append((child, child_weight))

    if balance_weight is None and children_with_bad_weight:
        if len(children_with_bad_weight) == 1:
            # Hit one of the children with the correct weight as expected weight
            child_to_correct, incorrect_weight = children_with_bad_weight[0]
            balance_weight = programs[child_to_correct].weight + (expected_weight - incorrect_weight)
        else:
            # Hit the one child with incorrect weight as expected weight
            correct_weight = children_with_bad_weight[0][1]
            balance_weight = programs[expected_weight_child_name].weight + (correct_weight - expected_weight)

    return weight, balance_weight


if __name__ == "__main__":
    main("input.txt")
