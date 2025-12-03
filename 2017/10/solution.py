def main(filename: str, knot_size: int = 256):
    with open(filename) as f:
        input_string = f.read().strip()

    raw_lengths = [int(_) for _ in input_string.split(",")]

    knot_hash, *_ = calc_knot_hash(lengths=raw_lengths, knot=list(range(knot_size)))
    print(f"The hash of the given knot is {knot_hash}.")

    dense_hash = calc_dense_knot_hash(input_string=input_string, knot_size=256)
    print(f"The dense hash for the input \"{input_string}\" is {dense_hash}.")


def calc_dense_knot_hash(input_string: str, knot_size: int = 256):
    dense_lengths = get_ascii_lengths(input_string)
    knot = list(range(knot_size))
    current_position = 0
    skip_size = 0

    for rnd in range(64):
        _, knot, current_position, skip_size = calc_knot_hash(
            lengths=dense_lengths,
            knot=knot,
            current_position=current_position,
            skip_size=skip_size,
        )

    dense = []
    for blocks in range(16):
        dense.append(0)
        for position in range(16):
            dense[-1] ^= knot[position + 16 * blocks]

    dense_knot_hash = "".join([hex(_)[2:].rjust(2, "0") for _ in dense])
    return dense_knot_hash


def calc_knot_hash(lengths: list[int], knot: list[int], current_position: int = 0, skip_size: int = 0) -> tuple[int, list[int], int, int]:
    knot_size = len(knot)
    for length in lengths:
        if length > knot_size:
            continue

        if length > 0:
            knot = reverse_subknot(knot=knot, current_position=current_position, length=length)

        current_position += length + skip_size
        current_position %= knot_size
        skip_size += 1

    return knot[0] * knot[1], knot, current_position, skip_size


def reverse_subknot(knot: list[int], current_position: int, length: int) -> list[int]:
    end = (current_position + length) % len(knot)
    if end <= current_position:
        reversed_subknot = reversed(knot[current_position:] + knot[:end])
    else:
        reversed_subknot = reversed(knot[current_position:end])

    for reversed_entry in reversed_subknot:
        knot[current_position % len(knot)] = reversed_entry
        current_position += 1

    return knot


def get_ascii_lengths(input_string: str) -> list[int]:
    lengths = [ord(_) for _ in input_string] + [17, 31, 73, 47, 23]

    return lengths


if __name__ == "__main__":
    test_cases = [
        ([0, 1, 2, 3, 4], 0, 3, [2, 1, 0, 3, 4]),
        ([2, 1, 0, 3, 4], 3, 4, [4, 3, 0, 1, 2]),
        ([4, 3, 0, 1, 2], 3, 1, [4, 3, 0, 1, 2]),
        ([4, 3, 0, 1, 2], 1, 5, [3, 4, 2, 1, 0]),
    ]

    for idx, (test_knot, test_position, test_length, expected_result) in enumerate(test_cases):

        result = reverse_subknot(knot=test_knot, current_position=test_position, length=test_length)

        try:
            assert result == expected_result
        except AssertionError:
            print(f"Test case {idx + 1}: expected {expected_result}, but got: {result}.")

    dense_test_cases = [
        ("", "a2582a3a0e66e6e86e3812dcb672a272"),
        ("AoC 2017", "33efeb34ea91902bb2f59c9920caa6cd"),
        ("1,2,3", "3efbe78a8d82f29979031a4aa0b16a9d"),
        ("1,2,4", "63960835bcdc130f0b66d7ff4f6a5a8e")
    ]

    for idx, (test_input, expected_hash) in enumerate(dense_test_cases):
        result_hash = calc_dense_knot_hash(input_string=test_input)
        try:
            assert result_hash == expected_hash
        except AssertionError:
            print(f"Test case {idx + 1}: expected {expected_hash}, but got: {result_hash}.")

    main("input.txt")
