import re


class Node:
    def __init__(self, x: int, y: int, used: int, available: int, usage: int):
        self._x = x
        self._y = y
        self._used = used
        self._available = available
        self._size = used + available
        self._usage = usage
        self._has_goal_data = False
        self._is_target = False

    @property
    def used(self) -> int:
        return self._used

    @property
    def available(self) -> int:
        return self._available

    @property
    def size(self) -> int:
        return self._size

    @property
    def usage(self) -> int:
        return self._usage

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def position(self) -> tuple[int, int]:
        return self._x, self._y

    @property
    def has_goal_data(self) -> bool:
        return self._has_goal_data

    @has_goal_data.setter
    def has_goal_data(self, value: bool):
        self._has_goal_data = value

    @property
    def is_target(self) -> bool:
        return self._is_target

    @is_target.setter
    def is_target(self, value: bool):
        self._is_target = value

    @property
    def is_huge(self):
        return self._size > 100

    def __str__(self):
        if self._has_goal_data:
            return " G "

        elif self._is_target:
            return "(.)"

        elif self._size > 100:
            return " # "

        elif self._used == 0:
            return " _ "

        return " . "

    def __lt__(self, other: "Node"):
        return self.position < other.position

    @classmethod
    def from_string(cls, description) -> "Node":
        re_match = re.match(r"/dev/grid/node-x(\d+)-y(\d+)\s+\d+T\s+(\d+)T\s+(\d+)T\s+(\d+)%", description)

        return cls(
            x=int(re_match.group(1)),
            y=int(re_match.group(2)),
            used=int(re_match.group(3)),
            available=int(re_match.group(4)),
            usage=int(re_match.group(5)),
        )


def display_grid(nodes: list[Node]):
    dim_y = max(_.y for _ in nodes)

    for line in range(dim_y):
        line_nodes = [_ for _ in nodes if _.y == line]
        print("".join(str(_) for _ in sorted(line_nodes)))


def find_minimum_swaps(nodes: list[Node], target: tuple[int, int]) -> int:
    """
    Analysis of the grid showed, that there is exactly one wall in the way of our empty node to be passed around.
    The plan is simple:
      1) Find the first node in the row with the wall.
      2) Move the empty node to that position
      3) Move that empty node right next to the goal data node
      4) Move the goal data to the target node like this:
         . _ G  . G _  . G .  . G .  . G .  _ G .
         . . .  . . .  . . _  . _ .  _ . .  . . .
    Note that all moving happens in Manhattan metric!
    """
    target_x, _ = target
    max_x = max([node.x for node in nodes])
    goal_data_at_x, goal_data_at_y = (max_x, 0)
    zero_node_at_x, zero_node_at_y = [_ for _ in nodes if _.used == 0][0].position

    wall_y = max([_.y for _ in nodes if _.is_huge])
    connection_x = max([_.x for _ in nodes if _.y == wall_y and not _.is_huge])
    [_ for _ in nodes if _.position == (connection_x, wall_y)][0].is_target = True

    # Move empty node to the wall node
    min_swaps = abs(connection_x - zero_node_at_x) + abs(wall_y - zero_node_at_y)
    # Move it right next to goal data
    min_swaps += abs(connection_x - goal_data_at_x) + abs(wall_y - goal_data_at_y) - 1
    print(min_swaps)
    # Moving the data to the target
    min_swaps += (abs(goal_data_at_x - target_x) - 1) * 5 + 1

    return min_swaps


def main(filename: str):
    with open(filename) as f:
        nodes = [Node.from_string(_) for _ in f.readlines()[2:]]

    viable_pairs = 0

    for node in nodes:
        if node.used == 0:
            continue

        viable_pairs += len([partner for partner in nodes if partner is not node and partner.available >= node.used])

    print(f"There are {viable_pairs} viable pairs.")

    minimal_swaps = find_minimum_swaps(nodes, target=(0, 0))
    print(f"It requires at least {minimal_swaps} swaps to access the data.")


if __name__ == "__main__":
    main("input.txt")
