class AssignmentRange:
    def __init__(self, start: int, end: int):
        self._start = start
        self._end = end

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    def __contains__(self, other: 'AssignmentRange') -> bool:
        return self._start <= other.start and self._end >= other.end

    def overlaps(self, other: 'AssignmentRange') -> bool:
        return self._start <= other.start <= self._end or other.start <= self._start <= other.end
