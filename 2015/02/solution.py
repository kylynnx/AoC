import itertools
import math


def read_presents(filename: str) -> list[str]:
    with open(filename) as f:
        return f.readlines()


def read_single_present(present_str: str) -> list[int]:
    sides = [int(_) for _ in present_str.split("x")]
    sides.sort()
    return sides


def calculate_wrap_size(edges: list[int]) -> int:
    faces = [a * b for a, b in itertools.combinations(edges, 2)]
    faces.sort()
    smallest_area = faces[0]

    wrap_sizes = [2 * _ for _ in faces]
    return sum(wrap_sizes) + smallest_area


def calculate_ribbon_length(edges: list[int]) -> int:
    ribbon_length = 2 * (edges[0] + edges[1])
    ribbon_length += math.prod(edges)

    return ribbon_length


def main(filename: str):
    presents = read_presents(filename)

    wrap_area = 0
    ribbon_length = 0

    for present in presents:
        read_present = read_single_present(present)
        wrap_area += calculate_wrap_size(read_present)
        ribbon_length += calculate_ribbon_length(read_present)

    print(f"Wrap area: {wrap_area}")
    print(f"Ribbon length: {ribbon_length}")


if __name__ == '__main__':
    main("input.txt")
