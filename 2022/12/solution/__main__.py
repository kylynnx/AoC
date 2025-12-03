from typing import Tuple

from dijkstar import find_path, Graph, NoPathError

from graph_builder import GraphBuilder


def get_path_length(graph: Graph, start: Tuple[int, int], target: Tuple[int, int]) -> int:
    path = find_path(graph=graph, s=start, d=target)
    return path.total_cost


def main(filename: str):
    graph_builder = GraphBuilder(filename)
    graph, start, target = graph_builder.build()
    path_lengths = set()

    part_1_path_length = get_path_length(graph=graph, start=start, target=target)
    print(part_1_path_length)

    path_lengths.add(part_1_path_length)
    for new_start in graph_builder.optional_starts:
        try:
            path_lengths.add(get_path_length(graph=graph, start=new_start, target=target))
        except NoPathError:
            continue

    print(min(path_lengths))


if __name__ == '__main__':
    main('../input.txt')
