from typing import List, TextIO


class Range:
    def __init__(self, start: int, length: int):
        self._start = start
        self._length = length
        self._end = start + length

    @property
    def id_list(self) -> List[int]:
        return list(range(self._start, self._start + self._length))

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def __contains__(self, item: int) -> bool:
        if not isinstance(item, int):
            raise NotImplemented

        return self._start <= item < self._end

    def __str__(self):
        return f'{self._start} - {self._end}'


class MapEntry:
    def __init__(self, *, destination_start: int, source_start: int, length: int):
        self._source_range = Range(start=source_start, length=length)
        self._offset = destination_start - source_start
        self._length = length

    def __contains__(self, item: int) -> bool:
        if not isinstance(item, int):
            raise NotImplemented

        return item in self._source_range

    def __call__(self, source: int):
        return source + self._offset

    @property
    def start(self):
        return self._source_range.start

    @property
    def end(self):
        return self._source_range.end

    @property
    def length(self):
        return self._length


class Map:
    def __init__(self, file: TextIO, *, start: str):
        self._mapping = {}

        while start not in file.readline():
            pass

        while (_content := file.readline()) not in ['', '\n']:
            destination, source, length = (int(_) for _ in _content.split(' '))
            self._mapping[source] = MapEntry(destination_start=destination, source_start=source, length=length)

    def __call__(self, source: int) -> int:
        smaller_keys = [_ for _ in self._mapping.keys() if _ <= source]

        if smaller_keys:
            _lookup_key = max(smaller_keys)
            if source in self._mapping[_lookup_key]:
                return self._mapping[_lookup_key](source)

        return source
