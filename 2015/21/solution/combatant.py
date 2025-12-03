class Combatant:
    def __init__(self):
        self._hit_points = 0
        self._damage = 0
        self._armor = 0

    @property
    def hit_points(self):
        return self._hit_points

    @property
    def damage(self):
        return self._damage

    @property
    def armor(self):
        return self._armor