from enum import Enum


class HexCoordinate:
    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s

    def __str__(self):
        return f"q={self.q}, r={self.r}, s={self.s}"

    def __add__(self, other: "HexCoordinate") -> "HexCoordinate":
        return HexCoordinate(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other: "HexCoordinate") -> "HexCoordinate":
        return HexCoordinate(self.q - other.q, self.r - other.r, self.s - other.s)

    @property
    def distance_to_origin(self) -> int:
        return max(abs(self.q), abs(self.r), abs(self.s))

class Direction(Enum):
    n = HexCoordinate(q=0, r=-1, s=1)
    ne = HexCoordinate(q=1, r=-1, s=0)
    se = HexCoordinate(q=1, r=0, s=-1)
    s = HexCoordinate(q=0, r=1, s=-1)
    sw = HexCoordinate(q=-1, r=1, s=0)
    nw = HexCoordinate(q=-1, r=0, s=1)


def main(filename: str):
    with open(filename) as f:
        directions = [Direction[_] for _ in f.read().strip().split(",")]

    child_position = HexCoordinate(0, 0, 0)
    max_distance = 0

    for direction in directions:
        child_position += direction.value

        if child_position.distance_to_origin > max_distance:
            max_distance = child_position.distance_to_origin

    print(f"It takes {child_position.distance_to_origin} steps to reach the child.")
    print(f"On its way the largest distance the child ever was from the origin is {max_distance} steps away.")


if __name__ == "__main__":
    main("input.txt")
