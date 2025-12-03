from enum import Enum


class ObjectType(Enum):
    ROUND_ROCK = 'O'
    CUBE_ROCK = '#'
    EMPTY = '.'


class Platform:
    def __init__(self, filename: str):
        with open(filename, 'r') as _f:
            self._platform_rows = [_.strip('\n') for _ in _f.readlines()]
        self._row_length = len(self._platform_rows[0])
        self._row_count = len(self._platform_rows)
        self._load = None

    def _transpose(self):
        _transposed = []
        for row_index in range(len(self._platform_rows[0])):
            _transposed.append(''.join([_[row_index] for _ in self._platform_rows]))
        self._platform_rows = _transposed

    def _mirror(self):
        _mirrored = []
        for row in self._platform_rows:
            _mirrored.append(row[::-1])
        self._platform_rows = _mirrored

    def _hash(self):
        return hash(''.join(self._platform_rows))

    @staticmethod
    def _tilt_row(row: str) -> str:
        _tilted_str = ''
        _empty_fields = 0
        _round_rocks = 0
        for position in row:
            match position:
                case ObjectType.CUBE_ROCK.value:
                    _tilted_str += (f'{ObjectType.ROUND_ROCK.value * _round_rocks}'
                                    f'{ObjectType.EMPTY.value * _empty_fields}'
                                    f'{ObjectType.CUBE_ROCK.value}')
                    _empty_fields = 0
                    _round_rocks = 0
                case ObjectType.ROUND_ROCK.value:
                    _round_rocks += 1
                case ObjectType.EMPTY.value:
                    _empty_fields += 1
        if row[-1] != ObjectType.CUBE_ROCK.value:
            _tilted_str += f'{ObjectType.ROUND_ROCK.value * _round_rocks}{ObjectType.EMPTY.value * _empty_fields}'
        return _tilted_str

    def _tilt_platform(self):
        _tilted_rows = []
        for row in self._platform_rows:
            _tilted_rows.append(self._tilt_row(row))
        self._platform_rows = _tilted_rows

    def tilt_north(self):
        self._transpose()
        self._tilt_platform()
        self._transpose()

    def tilt_west(self):
        # No rotations needed
        self._tilt_platform()

    def tilt_south(self):
        self._transpose()
        self._mirror()
        self._tilt_platform()
        self._mirror()
        self._transpose()

    def tilt_east(self):
        self._mirror()
        self._tilt_platform()
        self._mirror()

    @property
    def load(self):
        self._set_load()

        return self._load

    def _spin(self):
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def _set_load(self):
        _load = 0
        for row_index in range(self._row_count):
            _load += (self._row_count - row_index) * self._platform_rows[row_index].count(ObjectType.ROUND_ROCK.value)

        self._load = _load

    def spin_cycle(self, cycle_length: int):
        _hash = self._hash()
        _hashes = []
        _loads = []
        _done_cycles = 0

        while _hash not in _hashes and _done_cycles < cycle_length:
            _hashes.append(_hash)
            _loads.append(self.load)
            self._spin()
            _hash = self._hash()
            _done_cycles += 1

        if _done_cycles == cycle_length:
            return self.load

        _offset = _hashes.index(_hash)
        idempotence_cycle = len(_hashes) - _offset

        return _loads[(cycle_length - _offset) % idempotence_cycle + _offset]


def main_part_one(filename: str):
    platform = Platform(filename)
    platform.tilt_north()
    print(platform.load)


def main_part_tow(filename: str):
    platform = Platform(filename)
    print(platform.spin_cycle(1000000000))


if __name__ == '__main__':
    main_part_one('./input.txt')
    main_part_tow('./input.txt')
