from dijkstar import Graph
from networkx import DiGraph, all_simple_paths, path_weight

from graph_builder import GraphBuilder
from graph_directer import GraphDirecter


def di_graph_add_edge(graph: DiGraph, start, end, capacity):
    graph.add_edge(start, end, capacity=capacity)


def graph_add_edge(graph: Graph, start, end, weight):
    graph.add_edge(start, end, weight)


def slippery_slopes(filename: str):
    graph_builder = GraphBuilder(filename, DiGraph, {}, di_graph_add_edge)
    graph = graph_builder.graph
    all_paths = all_simple_paths(graph, source=graph_builder.start, target=graph_builder.end)
    path_weights = [path_weight(graph, _, 'capacity') for _ in all_paths]
    print(max(path_weights))


def no_slopes(filename: str):
    graph_builder = GraphBuilder(filename, Graph, {'undirected': True}, graph_add_edge)
    undirected_graph = graph_builder.graph
    start = graph_builder.start
    end = graph_builder.end
    directed_graph = GraphDirecter.direct(undirected_graph, start, end, DiGraph, {}, di_graph_add_edge)
    all_paths = all_simple_paths(directed_graph, source=graph_builder.start, target=graph_builder.end)
    path_weights = [path_weight(directed_graph, _, 'capacity') for _ in all_paths]
    print(max(path_weights))


def main(filename: str):
    slippery_slopes(filename)
    no_slopes('../input.txt')


if __name__ == '__main__':
    main('../input.txt')
