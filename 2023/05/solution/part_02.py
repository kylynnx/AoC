import operator
import re
from typing import TextIO, Union, List

from common_definitions import Range, Map


class SeedRangeList:
    def __init__(self, file: TextIO):
        _content = file.readline()
        match = re.match(r'seeds: (.*)$', _content)
        _content_list = match.group(1).split(' ')
        self._seed_ranges = [Range(int(_), int(__)) for _, __ in zip(_content_list[::2], _content_list[1::2])]
        self._seed_ids = []

    @property
    def seeds(self):
        if not self._seed_ids:
            for _range in self._seed_ranges:
                self._seed_ids += _range.id_list

        return self._seed_ids

    @property
    def seed_ranges(self):
        return self._seed_ranges


class RangedMap(Map):
    def __call__(self, source: Union[int, Range]) -> Union[int, List[Range]]:
        if isinstance(source, int):
            return super().__call__(source)

        _ranges = []
        _current_start = source.start
        _source_end = source.end
        while _current_start < _source_end:
            _left_keys = [_ for _ in self._mapping.keys() if _ <= _current_start]
            _left_lookup = self._mapping[max(_left_keys)] if _left_keys else None
            _right_keys = [_ for _ in self._mapping.keys() if _ > _current_start]
            _right_lookup = self._mapping[min(_right_keys)] if _right_keys else None

            if _left_lookup and _left_lookup.end > _current_start:
                _start = _left_lookup(_current_start)
                if _left_lookup.end <= _source_end:
                    _end = _left_lookup(_left_lookup.end)
                else:
                    _end = _left_lookup(_source_end)
            elif _right_lookup and _right_lookup.start < _source_end:
                _start = _current_start
                _end = _right_lookup.start
            else:
                _start = _current_start
                _end = _source_end

            _length = _end - _start
            _ranges.append(Range(start=_start, length=_length))
            _current_start += _length

        return _ranges


class RangedAlmanac:
    def __init__(self, file: TextIO):
        self._seed_ranges = SeedRangeList(file)
        self._seed_to_soil_map = RangedMap(file, start='seed-to-soil')
        self._soil_to_fertilizer_map = RangedMap(file, start='soil-to-fertilizer')
        self._fertilizer_to_water_map = RangedMap(file, start='fertilizer-to-water')
        self._water_to_light_map = RangedMap(file, start='water-to-light')
        self._light_to_temperature_map = RangedMap(file, start='light-to-temperature')
        self._temperature_to_humidity_map = RangedMap(file, start='temperature-to-humidity')
        self._humidity_to_location_map = RangedMap(file, start='humidity-to-location')

        self._soil_ranges = None
        self._fertilizer_ranges = None
        self._water_ranges = None
        self._light_ranges = None
        self._temperature_ranges = None
        self._humidity_ranges = None
        self._location_ranges = None

    def map(self, source: int) -> int:
        _soil = self._seed_to_soil_map(source)
        _fertilizer = self._soil_to_fertilizer_map(_soil)
        _water = self._fertilizer_to_water_map(_fertilizer)
        _light = self._water_to_light_map(_water)
        _temperature = self._light_to_temperature_map(_light)
        _humidity = self._temperature_to_humidity_map(_temperature)
        _location = self._humidity_to_location_map(_humidity)

        return _location

    @property
    def seeds(self):
        return self._seed_ranges.seeds

    @property
    def locations(self):
        return [self.map(_) for _ in self.seeds]

    @property
    def seed_ranges(self):
        return self._seed_ranges.seed_ranges

    @property
    def soil_ranges(self):
        if not self._soil_ranges:
            _soil_ranges = []
            for seed_range in self.seed_ranges:
                _soil_ranges += self._seed_to_soil_map(seed_range)
            self._soil_ranges = _soil_ranges

        return self._soil_ranges

    @property
    def fertilizer_ranges(self):
        if not self._fertilizer_ranges:
            _fertilizer_ranges = []
            for soil_range in self.soil_ranges:
                _fertilizer_ranges += self._soil_to_fertilizer_map(soil_range)
            self._fertilizer_ranges = _fertilizer_ranges

        return self._fertilizer_ranges

    @property
    def water_ranges(self):
        if not self._water_ranges:
            _water_ranges = []
            for fertilizer_range in self.fertilizer_ranges:
                _water_ranges += self._fertilizer_to_water_map(fertilizer_range)
            self._water_ranges = _water_ranges

        return self._water_ranges

    @property
    def light_ranges(self):
        if not self._light_ranges:
            _light_ranges = []
            for water_range in self.water_ranges:
                _light_ranges += self._water_to_light_map(water_range)
            self._light_ranges = _light_ranges

        return self._light_ranges

    @property
    def temperature_ranges(self):
        if not self._temperature_ranges:
            _temperature_ranges = []
            for light_range in self.light_ranges:
                _temperature_ranges += self._light_to_temperature_map(light_range)
            self._temperature_ranges = _temperature_ranges

        return self._temperature_ranges

    @property
    def humidity_ranges(self):
        if not self._humidity_ranges:
            _humidity_ranges = []
            for temperature_range in self.temperature_ranges:
                _humidity_ranges += self._temperature_to_humidity_map(temperature_range)
            self._humidity_ranges = _humidity_ranges

        return self._humidity_ranges

    @property
    def location_ranges(self):
        if not self._location_ranges:
            _location_ranges = []
            for humidity_range in self.humidity_ranges:
                _location_ranges += self._humidity_to_location_map(humidity_range)
            self._location_ranges = _location_ranges

        return self._location_ranges

    @property
    def min_location(self):
        _locations = self.location_ranges
        _locations.sort(key=operator.attrgetter("start"))
        return _locations[0].start


def main(filename: str):
    with open(filename, 'r') as _f:
        almanac = RangedAlmanac(_f)

    print(almanac.min_location)


if __name__ == '__main__':
    main('../input.txt')
