from itertools import combinations


def main(filename: str):
    with open(filename) as f:
        lines = [[int(n)  for n in _.strip("\n").split("\t")] for _ in f.readlines()]

    checksum = calculate_min_max_checksum(lines)
    print(f"The checksum is {checksum}.")

    checksum = calculate_evenly_divisible_checksum(lines)
    print(f"The second checksum is {checksum}.")


def calculate_min_max_checksum(lines: list[list[int]]) -> int:
    checksum = 0

    for line in lines:
        checksum += max(line) - min(line)

    return checksum


def calculate_evenly_divisible_checksum(lines: list[list[int]]) -> int:
    checksum = 0

    for line in lines:
        for x, y in combinations(line, 2):
            if x > y and x % y == 0:
                checksum += x // y
            elif y % x == 0:
                checksum += y // x

    return checksum


if __name__ == "__main__":
    main("input.txt")
