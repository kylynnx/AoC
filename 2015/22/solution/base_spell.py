from game_state_change import GameStateChange
from spell_type import SpellType


class BaseSpell:
    spell_type: SpellType = None

    cost: int = None
    _turns_active: int = 0
    _effect_on_cast: GameStateChange = None
    _effect_on_turn: GameStateChange = None
    _effect_on_end: GameStateChange = None


    def __init__(self, turns_left: int | None = None):
        self._turns_left = turns_left or self._turns_active

    @property
    def turns_left(self):
        return self._turns_left

    def advance_turn(self):
        self._turns_left -= 1

    @property
    def effect_on_cast(self):
        return self._effect_on_cast

    @property
    def effect_on_turn(self):
        return self._effect_on_turn

    @property
    def effect_on_end(self):
        return self._effect_on_end

    def copy(self):
        return self.__class__(self.turns_left)
