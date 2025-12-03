def is_open(x: int, y: int) -> bool:
    n = x * x + 3 * x + 2 * x * y + y + y * y + 1350
    bits = bin(n)
    return bits.count("1") % 2 == 0


def main(start: tuple[int, int], target: tuple[int, int]):
    path_length = find_path_length(start=start, target=target)
    print(f"It takes {path_length} steps to reach {target}.")

    visited_field_count = get_visited_field_count(start=start, max_moves=50)
    print(f"In the first 50 steps, there are {visited_field_count} visited fields.")


def get_adjacent_fields(current: list[tuple[int, int]], reached: set[tuple[int, int]]) -> list[tuple[int, int]]:
    return_list = []
    for position in current:
        for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_position = (position[0] + move[0], position[1] + move[1])
            if new_position not in reached and is_open(*new_position) and new_position[0] >= 0 and new_position[1] >= 0:
                reached.add(new_position)
                return_list.append(new_position)

    return return_list


def find_path_length(start: tuple[int, int], target: tuple[int, int]) -> int:
    reached = set()
    reached.add(start)
    moves = 0
    current = [start]
    while target not in reached:
        moves += 1
        current = get_adjacent_fields(current=current, reached=reached)

    return moves


def get_visited_field_count(start: tuple[int, int], max_moves: int) -> int:
    reached = set()
    reached.add(start)
    moves = 0
    current = [start]
    while moves < max_moves:
        moves += 1
        current = get_adjacent_fields(current=current, reached=reached)
    return len(reached)


if __name__ == '__main__':
    main(target=(31, 39), start=(1, 1))
