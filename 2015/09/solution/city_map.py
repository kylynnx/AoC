class CityMap:
    def __init__(self):
        self._map: dict[str, dict[str, int]] = {}
        self._cities: list[str] = []

    @property
    def cities(self):
        return self._cities

    def add_connection(self, city_one: str, city_two: str, distance: int):
        if city_one not in self._cities:
            self._cities.append(city_one)
            self._map[city_one] = {}

        if city_two not in self._cities:
            self._cities.append(city_two)
            self._map[city_two] = {}

        self._map[city_one][city_two] = distance
        self._map[city_two][city_one] = distance

    def get_distance(self, city_one: str, city_two: str) -> int:
        return self._map[city_one][city_two]

    def get_path_distance(self, path: tuple[str, ...]) -> int:
        distance = 0
        city_b = path[0]

        for city_index in range(1, len(path)):
            city_a = city_b
            city_b = path[city_index]
            distance += self.get_distance(city_a, city_b)

        return distance
