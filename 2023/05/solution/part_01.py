import re
from typing import TextIO

from common_definitions import Map


class SeedList:
    def __init__(self, file: TextIO):
        _content = file.readline()
        match = re.match(r'seeds: (.*)$', _content)
        _content_list = match.group(1).split(' ')

        self._seed_ids = [int(_) for _ in _content_list]

    @property
    def seeds(self):
        return self._seed_ids


class Almanac:
    def __init__(self, file: TextIO):
        self._seed_list = SeedList(file)
        self._seed_to_soil_map = Map(file, start='seed-to-soil')
        self._soil_to_fertilizer_map = Map(file, start='soil-to-fertilizer')
        self._fertilizer_to_water_map = Map(file, start='fertilizer-to-water')
        self._water_to_light_map = Map(file, start='water-to-light')
        self._light_to_temperature_map = Map(file, start='light-to-temperature')
        self._temperature_to_humidity_map = Map(file, start='temperature-to-humidity')
        self._humidity_to_location_map = Map(file, start='humidity-to-location')

        self._soils = None
        self._fertilizers = None
        self._waters = None
        self._lights = None
        self._temperatures = None
        self._humidities = None
        self._locations = None

    @property
    def seeds(self):
        return self._seed_list.seeds

    @property
    def soils(self):
        if not self._soils:
            self._soils = [self._seed_to_soil_map(_) for _ in self.seeds]

        return self._soils

    @property
    def fertilizers(self):
        if not self._fertilizers:
            self._fertilizers = [self._soil_to_fertilizer_map(_) for _ in self.soils]

        return self._fertilizers

    @property
    def waters(self):
        if not self._waters:
            self._waters = [self._fertilizer_to_water_map(_) for _ in self.fertilizers]

        return self._waters

    @property
    def lights(self):
        if not self._lights:
            self._lights = [self._water_to_light_map(_) for _ in self.waters]

        return self._lights

    @property
    def temperatures(self):
        if not self._temperatures:
            self._temperatures = [self._light_to_temperature_map(_) for _ in self.lights]

        return self._temperatures

    @property
    def humidities(self):
        if not self._humidities:
            self._humidities = [self._temperature_to_humidity_map(_) for _ in self.temperatures]

        return self._humidities

    @property
    def locations(self):
        if not self._locations:
            self._locations = [self._humidity_to_location_map(_) for _ in self.humidities]

        return self._locations


def main(filename: str):
    with open(filename, 'r') as _f:
        almanac = Almanac(_f)

    print(min(almanac.locations))


if __name__ == '__main__':
    main('../input.txt')
