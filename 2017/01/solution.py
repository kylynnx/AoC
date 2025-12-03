def count_matches(digits: list[int], offset: int = 1) -> int:
    matches = 0
    len_digits = len(digits)
    for position in range(len(digits)) :
        if digits[position] == digits[(position + offset) % len_digits]:
            matches += digits[position]

    return matches


def main(filename: str):
    with open(filename) as f:
        digits = [int(_) for _ in f.read().strip("\n")]
    print(f"The first captcha solution is {count_matches(digits)}.")
    print(f"The second captcha solution is {count_matches(digits, len(digits) // 2)}.")


if __name__ == "__main__":
    main("input.txt")
