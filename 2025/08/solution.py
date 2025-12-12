from itertools import combinations
from math import sqrt, prod
from typing import NamedTuple


class JunctionBox(NamedTuple):
    x: int
    y: int
    z: int

    def __sub__(self, other: JunctionBox) -> JunctionBox:
        return JunctionBox(self.x - other.x, self.y - other.y, self.z - other.z)

    def __abs__(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


def main(filename: str, connections: int):
    with open(filename) as f:
        junctions = [JunctionBox(*[int(_) for _ in line.split(",")]) for line in f.readlines()]

    distances = []
    for left, right in combinations(junctions, 2):
        distances.append((abs(left - right), left, right))
    distances.sort(key=lambda c: c[0])

    circuits = [{_} for _ in junctions]
    made_connections = 0
    sizes_product = 0
    last_connection = None

    while len(circuits) > 1:
        made_connections += 1
        _, left, right = distances.pop(0)
        last_connection = (left, right)

        contains_left = [_ for _ in circuits if left in _]
        contains_right = [_ for _ in circuits if right in _]

        if not contains_right and not contains_left:
            circuits.append({left, right})
        elif contains_left and not contains_right:
            [_.add(right) for _ in contains_left]
        elif contains_right and not contains_left:
            [_.add(left) for _ in contains_right]
        else:
            left = contains_left.pop()
            right = contains_right.pop()

            if left != right:
                circuits.remove(left)
                circuits.remove(right)
                circuits.append(left.union(right))

        if made_connections == connections:
            sizes = [len(_) for _ in circuits]
            sizes.sort(reverse=True)
            sizes_product = prod(sizes[0: 3])

    last_connection_identifier = prod(_.x for _ in last_connection) if last_connection is not None else None
    print(f"The product of the sizes is {sizes_product}.")
    print(f"The last connection is identified by {last_connection_identifier}.")


if __name__ == "__main__":
    main("test.txt", connections=10)
    main("input.txt", connections=1000)
