from dijkstar import find_path

from graph_factory import GraphFactory
from heat_loss_map import HeatLossMap


def main(filename: str):
    heat_loss_map = HeatLossMap(filename)
    start = (0, 0)
    end = (heat_loss_map.dim_x - 1, heat_loss_map.dim_y - 1)
    graph_factory = GraphFactory(min_steps=0, max_steps=3)
    graph = graph_factory.get_graph(heat_loss_map=heat_loss_map)
    path_info = find_path(graph=graph, s=start, d=end)
    print(path_info.total_cost)


if __name__ == '__main__':
    main('../input.txt')
