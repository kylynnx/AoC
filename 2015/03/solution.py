from enum import Enum


class Move(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


def read_moves(filename: str) -> list[Move]:
    with open(filename) as f:
        move_set = f.read()

    moves = [Move(_) for _ in move_set]
    return moves


def perform_move(x: int, y: int, move: Move) -> (int, int):
    match move:
        case Move.UP:
            return x, y + 1
        case Move.DOWN:
            return x, y - 1
        case Move.LEFT:
            return x - 1, y
        case Move.RIGHT:
            return x + 1, y
        case _:
            raise ValueError(f"{x}, {y}, {move}")


def get_moves_statistics(moves, visited_coordinates = None):
    current_x = 0
    current_y = 0

    if visited_coordinates is None:
        visited_coordinates = {(current_x, current_y)}

    for move in moves:
        current_x, current_y = perform_move(current_x, current_y, move)
        visited_coordinates.add((current_x, current_y))

    return visited_coordinates


def main_one(moves: list[Move]):
    print(len(get_moves_statistics(moves)))


def main_two(moves: list[Move]):
    santa_moves = moves[::2]
    robot_moves = moves[1::2]

    visited_santa = get_moves_statistics(santa_moves)
    visited = get_moves_statistics(robot_moves, visited_santa)

    print(len(visited))


def main(filename: str):
    moves = read_moves(filename)
    main_one(moves)
    main_two(moves)


if __name__ == '__main__':
    main("input.txt")
