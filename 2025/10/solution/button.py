from lights import Lights


class Button:
    def __init__(self, toggles: set[int]):
        self._toggles = toggles

    @property
    def numeric(self):
        return sum(2 ** _ for _ in self._toggles)

    @property
    def toggles(self) -> set[int]:
        return self._toggles

    def apply(self, lights: Lights) -> Lights:
        new_lights = [_ for _ in lights]

        for position in self._toggles:
            new_lights[position] ^= True

        return Lights(new_lights)
