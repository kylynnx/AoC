def main(steps: int, insertions: int = 2017):
    buffer = [0, 1]
    current = 1
    count_insertions = 1

    while count_insertions <= insertions:
        count_insertions += 1
        insertion_position = (current + steps) % len(buffer)
        buffer = buffer[:insertion_position + 1] + [count_insertions] + buffer[insertion_position + 1:]
        current = insertion_position + 1

    value_after_2017 = buffer[(buffer.index(2017) + 1) % len(buffer)]
    print(f"The value right after 2017 is {value_after_2017}.")

    current = 0
    value_after_zero = None

    for spins in range(1, 50000000):
        current = ((current + steps) % spins) + 1
        if current == 1:
            value_after_zero = spins

    print(f"After 50 million spins the value after zero is {value_after_zero}.")


if __name__ == "__main__":
    main(steps=3)
    main(steps=354)
