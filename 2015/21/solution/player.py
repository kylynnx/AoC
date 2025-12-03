from combatant import Combatant
from loadout import Loadout


class Player(Combatant):
    def __init__(self):
        super().__init__()

        self._hit_points = 100
        self._loadout = None

    @property
    def damage(self):
        if self._loadout is not None:
            return self._damage + self._loadout.damage

        return self._damage

    @property
    def armor(self):
        if self._loadout is not None:
            return self._armor + self._loadout.armor

        return self._armor

    def don_loadout(self, loadout: Loadout):
        self._loadout = loadout

    def doff_loadout(self):
        self._loadout = None

    def beats(self, enemy: Combatant) -> bool:
        rounds_player = enemy.hit_points // max(self.damage - enemy.armor, 1) + 1
        boss_rounds = self._hit_points // max(enemy.damage - self.armor, 1) + 1

        return rounds_player <= boss_rounds
