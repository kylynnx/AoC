class GameStateChange:
    def __init__(self, player_hp_change: int = 0, player_mana_change: int = 0, player_armor_change: int = 0,
                 boss_hp_change: int = 0):
        self._player_hp_change = player_hp_change
        self._player_mana_change = player_mana_change
        self._player_armor_change = player_armor_change
        self._boss_hp_change = boss_hp_change

    @property
    def player_hp_change(self):
        return self._player_hp_change

    @property
    def player_mana_change(self):
        return self._player_mana_change

    @property
    def player_armor_change(self):
        return self._player_armor_change

    @property
    def boss_hp_change(self):
        return self._boss_hp_change