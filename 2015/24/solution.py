from itertools import combinations
from math import prod


def get_min_quantum_entanglement(packages: list[int], group_weight: int) -> int | None:
    package_count = len(packages)

    for group_size in range(package_count):
        groups_with_size = [_ for _ in combinations(packages, r=group_size) if sum(_) == group_weight]

        if groups_with_size:
            quantum_entanglements = [prod(_) for _ in groups_with_size]

            return min(quantum_entanglements)

    return None


def main(filename: str, groups: int):
    with open(filename, "r") as f:
        packages = [int(_) for _ in f.readlines()]

    group_weight = sum(packages) // groups

    min_quantum_entanglement = get_min_quantum_entanglement(packages=packages, group_weight=group_weight)

    print(f"Minimal quantum entanglement: {min_quantum_entanglement}")


if __name__ == '__main__':
    main("input.txt", 3)
    main("input.txt", 4)
