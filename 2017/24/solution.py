from collections import defaultdict
from math import prod


def main(filename: str):
    with open(filename) as f:
        components_strings = [_.strip() for _ in f.readlines()]

    components = set()
    for component in components_strings:
        p, q = component.split("/")
        components.add((int(p), int(q)))

    bridges = build_bridges(start_pin_count=0, components=components)
    strengths = {sum(sum(c) for c in bridge): bridge for bridge in bridges}
    print(f"The strongest bridge has strength {max(strengths)}.")

    lengths = defaultdict(list)
    for bridge in bridges:
        lengths[len(bridge)].append(bridge)

    max_length = max(lengths)
    strength_max_length = max(sum(sum(c) for c in bridge) for bridge in lengths[max_length])
    print(f"The longest bridge has strength {strength_max_length}.")


def build_bridges(start_pin_count: int, components: set[tuple[int, int]]) -> list[set[tuple[int, int]]]:
    zero_pin_components = [_ for _ in components if start_pin_count in _]
    bridges = []

    queue = [(sum(_), {_}) for _ in zero_pin_components]

    while queue:
        pin_connections, used_components = queue.pop(0)

        available_components = [_ for _ in components - used_components if pin_connections in _]

        if not available_components:
            bridges.append(used_components)
            continue

        for component in available_components:
            connections = sum(component) - pin_connections
            new_used_components = set(used_components)
            new_used_components.add(component)
            queue.append((connections, new_used_components))

    return bridges


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
