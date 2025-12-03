from city_map import CityMap
from utility import deserialize_map_string
from path_finder import MinimalDistancePathFinder, MaximalDistancePathFinder


def main(filename: str):
    with open(filename) as f:
        map_entries = [deserialize_map_string(_.strip("\n")) for _ in f.readlines()]

    city_map = CityMap()
    for map_entry in map_entries:
        city_map.add_connection(*map_entry)

    minimal_path_finder = MinimalDistancePathFinder()
    maximal_path_finder = MaximalDistancePathFinder()

    minimal_path_finder.find_path(city_map)
    print(minimal_path_finder.optimal_distance)

    maximal_path_finder.find_path(city_map)
    print(maximal_path_finder.optimal_distance)


if __name__ == '__main__':
    main("../input.txt")
