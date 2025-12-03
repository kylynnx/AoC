import math
from abc import abstractmethod
from itertools import permutations

from city_map import CityMap


class PathFinder:
    def __init__(self, starting_distance: int | float):
        self._optimal_distance: int = starting_distance

    @property
    def optimal_distance(self) -> int:
        return self._optimal_distance

    def find_path(self, city_map: CityMap) -> (list[str], int):
        for path in permutations(city_map.cities, r=len(city_map.cities)):
            current_distance = city_map.get_path_distance(path)

            if self._accept_current_distance(current_distance):
                self._optimal_distance = current_distance

    @abstractmethod
    def _accept_current_distance(self, current_distance: int) -> bool:
        pass


class MinimalDistancePathFinder(PathFinder):
    def __init__(self):
        super().__init__(math.inf)

    def _accept_current_distance(self, current_distance: int) -> bool:
        if current_distance < self._optimal_distance:
            return True



class MaximalDistancePathFinder(PathFinder):
    def __init__(self):
        super().__init__(0)

    def _accept_current_distance(self, current_distance: int) -> bool:
        if current_distance > self._optimal_distance:
            return True
