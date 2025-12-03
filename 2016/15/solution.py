import re


def main(filename: str):
    with open(filename) as f:
        disc_strings = f.readlines()

    numbers = []
    remainders = []
    discs = get_discs(disc_strings)
    for idx, disc in enumerate(discs):
        start, positions = disc

        remainder = - start - idx -1
        while remainder < 0:
            remainder += positions

        numbers.append(positions)
        remainders.append(remainder)

    print(f"First button press at t={find_time_by_chinese_remainder_theorem(numbers, remainders)}s.")

    numbers.append(11)
    new_remainder = - len(remainders) - 1 - 0
    while new_remainder < 0:
        new_remainder += 11

    remainders.append(new_remainder)
    print(f"Second button press at t={find_time_by_chinese_remainder_theorem(numbers, remainders)}s.")



def get_discs(disc_strings: list[str]) -> list[tuple[int, int]]:
    discs = []
    for line in disc_strings:
        match = re.match(r"Disc #\d has (\d+) positions; at time=0, it is at position (\d+).", line)
        discs.append((int(match.group(2)), int(match.group(1))))

    return discs


def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def find_time_by_chinese_remainder_theorem(numbers: list[int], remainders: list[int]):
    prod = 1
    for n in numbers:
        prod *= n

    result = 0
    for i in range(len(numbers)):
        prod_i = prod // numbers[i]
        _, inv_i, _ = gcd_extended(prod_i, numbers[i])
        result += remainders[i] * prod_i * inv_i

    return result % prod


if __name__ == '__main__':
    main(filename="input.txt")
