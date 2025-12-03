# After shrinking the graph in the graph builder it has some form like:
# Start -  a - b - c - d - e
#          |   |   |   |   | \
#          f - A - B - C - D - g
#          |   |   |   |   |   |
#          h - E - F - G - H - k
#          |   |   |   |   |   |
#          m - K - M - N - P - n
#          |   |   |   |   |   |
#          p - Q - R - S - T - q
#            \ |   |   |   |   |
#              r - s - t - u - v - End
#
# Due to performance reasons we will restrict all nodes on the border to only move right and down. All other moves end
# in a configuration where crossing the path is required.

from typing import Tuple

from dijkstar import Graph


from direction import Direction

flip_direction = {
    Direction.DOWN: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN
}


class GraphDirecter:
    @staticmethod
    def direct(undirected_graph: Graph, start: Tuple[int, int], end: Tuple[int, int], graph_class, graph_class_keywords,
               edge_set):
        directed_graph = graph_class(**graph_class_keywords)

        undirected_data = undirected_graph.get_data()

        inner_nodes = [_ for _, targets in undirected_data.items() if len(targets) == 4]
        for node in inner_nodes:
            for target, weight in undirected_data[node].items():
                edge_set(directed_graph, node, target, weight)
                edge_set(directed_graph, target, node, weight)

        start_proxy_node = list(undirected_data[start].keys())[0]
        start_proxy_weight = undirected_data[start][start_proxy_node]
        edge_set(directed_graph, start, start_proxy_node, start_proxy_weight)

        next_nodes = [_ for _ in undirected_data[start_proxy_node].keys() if _ != start]

        for next_node in next_nodes:
            new_path = [start_proxy_node, next_node]
            edge_set(directed_graph, start_proxy_node, next_node, undirected_data[start_proxy_node][next_node])
            while end not in new_path:
                current_node = new_path[-1]
                new_nodes = [
                    _ for _ in undirected_data[current_node].keys()
                    if len(undirected_data[_]) != 4 and _ not in new_path
                ]

                if len(new_nodes) > 1:
                    edge_set(directed_graph, current_node, end, undirected_data[current_node][end])
                    new_path.append(end)
                else:
                    target = new_nodes[0]
                    edge_set(directed_graph, current_node, target, undirected_data[current_node][target])
                    new_path.append(target)

        return directed_graph
