from itertools import permutations

from networkx import DiGraph, topological_sort


def load_graph(filename) -> DiGraph:
    with open(filename) as f:
        connections = [_.strip() for _ in f.readlines()]

    graph = DiGraph()

    for connection in connections:
        source, destinations = connection.split(": ")

        for destination in destinations.split(" "):
            graph.add_edge(source, destination)

    return graph


def main(filename: str):
    graph = load_graph(filename)

    analytics_connections = count_paths(graph=graph, source="you", target="out")
    print(f"There are {analytics_connections} from 'you' to 'out'.")

    paths_fft_dac = count_paths_with_intermediate_nodes(
        graph=graph, source="svr", target="out", intermediate_nodes={"dac", "fft"}
    )
    print(f"A total of {paths_fft_dac} leads from 'svr' to 'out' via 'dac' and 'fft'.")


def count_paths(graph: DiGraph, source: str, target: str) -> int:
    """
    Note that the given graph is a directed acyclic graph.
    Topological sort means that if an edge (u,v) (read: u -> v) exists, u will be in the order before v.
    """
    ordered_nodes = list(topological_sort(graph))

    paths = {node: 0 for node in ordered_nodes}
    paths[source] = 1

    for node in ordered_nodes:
        for successor in graph[node]:
            paths[successor] += paths[node]

    return paths[target]


def count_paths_with_intermediate_nodes(graph: DiGraph, source: str, target: str, intermediate_nodes: set[str]) -> int:
    result = 0

    for permutation in permutations(intermediate_nodes):
        partial = 1
        previous = source

        for node in permutation:
            partial *= count_paths(graph, previous, node)
            previous = node

        partial *= count_paths(graph, previous, target)
        result += partial

    return result


if __name__ == "__main__":
    assert count_paths(load_graph("test_you_out.txt"), "you", "out") == 5
    assert count_paths_with_intermediate_nodes(
        load_graph("test_svr_out.txt"), "svr", "out", {"dac", "fft"}
    ) == 2

    main("input.txt")
