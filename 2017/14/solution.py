def main(key: str):
    used_spaces = 0
    grid = {}
    for row in range(128):
        knot_hash = calc_dense_knot_hash(f"{key}-{row}")
        hex_hash = int(knot_hash, 16)
        binary_string = bin(hex_hash)[2:]
        binary_string = binary_string.rjust(128, "0")
        spaces = [int(_) for _ in binary_string]
        used_spaces += sum(spaces)
        grid[row] = spaces

    print(f"The disk contains {used_spaces} used spaces.")

    regions = count_regions(grid=grid)
    print(f"It consists of {regions} regions.")


# copied from day 10... should refactor at some point
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


def find_connected_spaces(dimension: int, grid: dict[int, list[int]], row: int, column: int, seen_positions: set[tuple[int, int]]):
    if (row, column) in seen_positions or not grid[row][column]:
        return

    seen_positions.add((row, column))

    if row >  0:
        find_connected_spaces(
            dimension=dimension,
            grid=grid,
            row=row - 1,
            column=column,
            seen_positions=seen_positions
        )

    if column > 0:
        find_connected_spaces(
            dimension=dimension,
            grid=grid,
            row=row,
            column=column - 1,
            seen_positions=seen_positions
        )

    if row < dimension - 1:
        find_connected_spaces(
            dimension=dimension,
            grid=grid,
            row=row + 1,
            column=column,
            seen_positions=seen_positions
        )

    if column < dimension - 1:
        find_connected_spaces(
            dimension=dimension,
            grid=grid,
            row=row,
            column=column + 1,
            seen_positions=seen_positions
        )


def count_regions(grid: dict[int, list[int]]) -> int:
    dimension = len(grid)
    seen_positions = set()
    regions = 0

    for row in range(dimension):
        for column in range(dimension):
            if (row, column) in seen_positions or not grid[row][column]:
                continue

            regions += 1
            find_connected_spaces(
                row=row,
                column=column,
                grid=grid,
                seen_positions=seen_positions,
                dimension=dimension
            )

    return regions


if __name__ == "__main__":
    main("flqrgnkx")
    main("hxtvlmkl")
