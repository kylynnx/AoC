from itertools import combinations

from equipment import Equipment
from loadout import Loadout


class Shop:
    def __init__(self, armors: list[Equipment], rings: list[Equipment], weapons: list[Equipment]):
        self._armors = armors
        self._rings = rings
        self._weapons = weapons

    def __iter__(self):
        for armor in self._armors:
            for weapon in self._weapons:
                for rings in combinations(self._rings, 2):
                    yield Loadout(armor=armor, rings=rings, weapon=weapon)
