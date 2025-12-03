from equipment import Equipment


class Loadout:
    def __init__(self, armor: Equipment, rings: tuple[Equipment, Equipment], weapon: Equipment):
        self._armor = armor
        self._rings = rings
        self._weapon = weapon

    @property
    def damage(self) -> int:
        return sum(_.damage for _ in self._rings) + self._weapon.damage

    @property
    def armor(self) -> int:
        return sum(_.armor for _ in self._rings) + self._armor.armor

    @property
    def cost(self) -> int:
        return sum(_.cost for _ in self._rings) + self._armor.cost + self._weapon.cost
