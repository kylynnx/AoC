import random

from networkx import Graph, minimum_cut


def read_graph(filename: str) -> Graph:
    graph = Graph()
    with open(filename, 'r') as _f:
        raw_lines = [_.strip('\n') for _ in _f.readlines()]

    for raw_line in raw_lines:
        start_node, connected_nodes = raw_line.split(': ')
        for connected_node in connected_nodes.split(' '):
            graph.add_edge(start_node, connected_node, capacity=1)

    return graph


def find_cut(graph: Graph):
    minimal_cut = 100
    partition = None

    while minimal_cut > 3:
        node_one = random.choice(list(graph.nodes))
        node_two = random.choice(list(graph.nodes))

        minimal_cut, partition = minimum_cut(graph, node_one, node_two)

    return partition


def main(filename: str):
    graph = read_graph(filename)
    partition = find_cut(graph)
    print(len(partition[0]) * len(partition[1]))


if __name__ == '__main__':
    main('input.txt')
