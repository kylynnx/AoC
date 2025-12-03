from collections import defaultdict
from itertools import combinations, permutations

type Maze = list[str]
type Point = tuple[int, int]


def main(filename: str):
    with open(filename) as f:
        maze_lines = [_.strip("\n") for _ in f.readlines()]

    points_of_interest = get_points_of_interest(maze_lines)
    distances = get_differences_between_points(maze=maze_lines, points=points_of_interest)
    shortest_one_way_distance = None
    shortest_round_trip_distance = None
    perms = list(permutations(_ for _ in points_of_interest.keys() if _ != "0"))
    iteniearies = [["0"] + list(_) for _ in perms]

    for itenieary in iteniearies:
        distance = get_distance_for_itenieary(distances=distances, itenieary=itenieary)
        if shortest_one_way_distance is None or distance < shortest_one_way_distance:
            shortest_one_way_distance = distance

        round_trip_distance = distance + distances[itenieary[-1]]["0"]
        if shortest_round_trip_distance is None or round_trip_distance < shortest_round_trip_distance:
            shortest_round_trip_distance = round_trip_distance

    print(f"In {shortest_one_way_distance} steps all points can be visited.")
    print(f"The shortest round trip has {shortest_round_trip_distance} steps.")


def get_differences_between_points(maze: Maze, points: dict[str, Point]) -> dict[str, dict[str, int]]:
    point_pairs = list(combinations(points.keys(), 2))
    distances = defaultdict(dict)

    for start, end in point_pairs:
        distance = get_distance(maze=maze, start=points[start], end=points[end])
        distances[start][end] = distance
        distances[end][start] = distance

    return distances


def get_distance_for_itenieary(distances: dict[str, dict[str, int]], itenieary: list[str]) -> int:
    start = 0
    distance = 0

    while start < len(itenieary) - 1:
        distance += distances[itenieary[start]][itenieary[start + 1]]
        start += 1
    return distance


def get_distance(maze: Maze, start: Point, end: Point) -> int:
    visited = set()
    queue = [[start]]

    while queue:
        path = queue.pop(0)

        current = path[-1]

        if current == end:
            return len(path) - 1

        for neighbor in get_neighbors(maze=maze, point=current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    raise ValueError("No path found.")


def get_neighbors(maze: Maze, point: Point) -> list[Point]:
    x, y = point
    reachable_neighbors = []

    if (new_x := x - 1) >= 0 and maze[y][new_x] != "#":
        reachable_neighbors.append((new_x, y))

    if (new_x := x + 1) < len(maze[0]) and maze[y][new_x] != "#":
        reachable_neighbors.append((new_x, y))

    if (new_y := y - 1) >= 0 and maze[new_y][x] != "#":
        reachable_neighbors.append((x, new_y))

    if (new_y := y + 1) and maze[new_y][x] != "#":
        reachable_neighbors.append((x, new_y))

    return reachable_neighbors


def get_points_of_interest(maze_lines: Maze) -> dict[str, Point]:
    points_of_interest = {}
    for y, line in enumerate(maze_lines):
        for x, position in enumerate(line):
            try:
                int(position)
                points_of_interest[position] = (x, y)
            except ValueError:
                pass

    return points_of_interest


if __name__ == "__main__":
    main("input.txt")
