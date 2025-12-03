from enum import Enum


class Direction(Enum):
    R = complex(0, -1)
    L = complex(0, 1)


def turn_and_walk(turn_direction: Direction, distance: int, position: complex, previous_direction: complex) -> (complex, complex):
    next_direction = turn_direction.value * previous_direction

    position += next_direction * distance

    return position, next_direction


def deserialize_steps(steps: str) -> list[tuple[Direction, int]]:
    step_list = []

    for step in steps.split(", "):
        direction = Direction[step[0]]
        distance = int(step[1:])

        step_list.append((direction, distance))

    return step_list


def manhattan_distance(position: complex) -> complex:
    return int(abs(position.real) + abs(position.imag))


def main(filename: str):
    with open(filename, "r") as f:
        step_description = f.read()

    steps = deserialize_steps(step_description)

    current_direction = complex(0, 1)
    position = complex(0, 0)
    visited = set()
    visited.add(position)
    visited_twice = None

    for direction, distance in steps:
        previous_position = position
        position, current_direction = turn_and_walk(
            turn_direction=direction,
            distance=distance,
            position=position,
            previous_direction=current_direction,
        )

        if visited_twice is None:
            for step_size in range(1, distance + 1):
                visited_location = previous_position + (current_direction * step_size)
                if visited_location in visited:
                    visited_twice = visited_location

                visited.add(visited_location)

    block_count = manhattan_distance(position)
    distance_visited = manhattan_distance(visited_twice) if visited_twice is not None else None

    print(f"Minimum distance to go to the Easter Bunny HQ is {block_count} blocks.")
    print(f"The first position visited twice is {distance_visited} blocks away.")


if __name__ == '__main__':
    main("input.txt")
