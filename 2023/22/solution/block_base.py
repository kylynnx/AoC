class BlockBase:
    def __init__(self, start_x: int, end_x: int, start_y: int, end_y: int):
        self._fields = set()

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                self._fields.add((x, y))

    @property
    def fields(self):
        return self._fields

    def overlap(self, other: 'BlockBase'):
        return any([_ in other.fields for _ in self._fields])
