class Equipment:
    def __init__(self, damage: int, armor: int, cost: int):
        self._cost = cost
        self._damage = damage
        self._armor = armor

    @property
    def damage(self) -> int:
        return self._damage

    @property
    def armor(self) -> int:
        return self._armor

    @property
    def cost(self) -> int:
        return self._cost
