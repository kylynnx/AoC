from itertools import combinations


def read_input(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(_) for _ in f.readlines()]


def main(filename: str, use_minimal_combinations: bool = False):
    containers = read_input(filename)
    container_count = len(containers)
    combination_count = 0
    found_minimal = False

    for n_containers in range(2, container_count + 1):
        if found_minimal and use_minimal_combinations:
            break

        for selected_containers in combinations(containers, n_containers):
            if sum (_ for _ in selected_containers) == 150:
                found_minimal = True
                combination_count += 1

    print(combination_count)


if __name__ == "__main__":
    main("input.txt")
    main("input.txt", use_minimal_combinations=True)
