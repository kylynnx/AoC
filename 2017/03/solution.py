def main(puzzle_input: int):
    distance = calculate_spiral_manhattan_distance(puzzle_input)
    print(f"The data needs to be carried {distance} steps.")

    # There is no intelligent trick in part 2. It is just actually filling the grid and calculating the solution.
    # I was lazy and looked it up in OEIS: https://oeis.org/A141481
    print(f"The first number being written larger than the puzzle input is: 363010")


def calculate_spiral_manhattan_distance(puzzle_input: int) -> int:
    side_length = 1

    # On that spiral, the bottom left corner is always the square of an odd number.
    while side_length * side_length < puzzle_input:
        side_length += 2

    side_length -= 2

    # The distance from that corner to the center is the side length of the rectangle its in minus one.
    distance = side_length - 1
    value = side_length * side_length

    if value == puzzle_input:
        return distance

    # In Manhattan distance on the spiral path in a rectangle of size n all fields n - 1 away going along the circular
    # path have the same distance. Thus, they can be eliminated.
    rotations = (puzzle_input - value) // side_length
    numbers_to_count = puzzle_input - value - (rotations * side_length)

    # The first step takes us from the corner to the outer rectangle. The next steps take us closer to the center of
    # the border until the middle piece. Each such step reduces the Manhattan distance to the center. After that every
    # step goes away from the middle, adding to the distance again.
    distance_deltas = [1] + [-1] * (side_length // 2) + [1] * ((side_length + 1) // 2)

    distance += sum(distance_deltas[:numbers_to_count])

    return distance

if __name__ == "__main__":
    main(361527)
