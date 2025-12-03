from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __lt__(self, other):
        return True


allowed_directions = {
    Direction.UP: [Direction.UP, Direction.LEFT, Direction.RIGHT],
    Direction.DOWN: [Direction.DOWN, Direction.LEFT, Direction.RIGHT],
    Direction.LEFT: [Direction.UP, Direction.DOWN, Direction.LEFT],
    Direction.RIGHT: [Direction.UP, Direction.DOWN, Direction.RIGHT],
}

invert = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT
}
