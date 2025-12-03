import re
from subprocess import check_call


def deserialize_line(line: str):
    match = re.match(r"(\d{1,3})\s+(\d{1,3})\s+(\d{1,3})", line)
    return [int(match.group(1)), int(match.group(2)), int(match.group(3))]


def check_triangle(sides: list[int]) -> bool:
    sides.sort()
    return sides[0] + sides[1] > sides[2]


def load_file(filename: str):
    with open(filename) as f:
        return [_.strip("\n").strip(" ") for _ in f.readlines()]

def horizontal(filename: str):
    lines = load_file(filename)

    valid_triangles = 0
    for line in lines:
        sides = deserialize_line(line)

        if check_triangle(sides):
            valid_triangles += 1

    print(valid_triangles)


def vertical(filename: str):
    lines = load_file(filename)

    count_triangles = len(lines) // 3
    valid_triangles = 0

    for n_triangle in range(count_triangles):
        first_triangle = []
        second_triangle = []
        third_triangle = []

        for i_triangle in range(3):
            sides = deserialize_line(lines[n_triangle * 3 + i_triangle])
            first_triangle.append(sides[0])
            second_triangle.append(sides[1])
            third_triangle.append(sides[2])

        valid_triangles += check_triangle(first_triangle)
        valid_triangles += check_triangle(second_triangle)
        valid_triangles += check_triangle(third_triangle)

    print(valid_triangles)


def main(filename: str):
    horizontal(filename)
    vertical(filename)


if __name__ == '__main__':
    main("input.txt")
