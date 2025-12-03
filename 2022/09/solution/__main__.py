from rope import Rope
from move import Move

from coordinate import Coordinate


def main(filename: str):
    rope = Rope(length=2)
    long_rope = Rope(length=10)

    with open(filename) as _f:
        move_strings = [_.strip('\n') for _ in _f.readlines()]

    for move_string in move_strings:
        move = Move(move_string=move_string)
        rope.move(move)
        long_rope.move(move)

    print(rope.tail_visit_count)
    print(long_rope.tail_visit_count)


if __name__ == '__main__':
    main('../input.txt')
