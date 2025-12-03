from math import sqrt, ceil


def main():
    print(f"The `mul` instruction is invoked {63 * 63} times.")

    start = (65 * 100) + 100000
    end = start + 17000
    composite_numbers = count_composite_numbers(start=start, end=end, step=17)

    print(f"When the program halts, register `h` is left at {composite_numbers}.")


def count_composite_numbers(start: int, end: int, step: int) -> int:
    composite_numbers = 0

    for number in range(start, end + 1, step):
        root = ceil(sqrt(number))

        for divisor in range(2, root + 1):
            if number % divisor == 0:
                composite_numbers += 1
                break

    return composite_numbers


if __name__ == "__main__":
    main()
