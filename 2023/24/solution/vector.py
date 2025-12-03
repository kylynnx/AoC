class Vector:
    def __init__(self, x: int, y: int, z: int):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def z(self) -> int:
        return self._z

    def get_by_name(self, name: str) -> int:
        match name:
            case 'x':
                return self._x
            case 'y':
                return self._y

        return self._z
