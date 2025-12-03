from vector import Vector


class Trajectory:
    def __init__(self, position: Vector, velocity: Vector):
        self._position = position
        self._velocity = velocity
        self._slope_2d = None
        self._intercept_2d = None

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity

    @property
    def slope_2d(self):
        if self._slope_2d is None:
            self._slope_2d = self._velocity.y / self._velocity.x

        return self._slope_2d

    @property
    def intercept_2d(self):
        if self._intercept_2d is None:
            self._intercept_2d = self._position.y - self.slope_2d * self._position.x

        return self._intercept_2d

    def get_y(self, x: float):
        return self._slope_2d * x + self._intercept_2d
