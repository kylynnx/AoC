from base_spell import BaseSpell
from game_state_change import GameStateChange
from spell_type import SpellType

gain_mana = GameStateChange(player_mana_change=101)


class Recharge(BaseSpell):
    spell_type = SpellType.RECHARGE
    cost = 229
    _turns_active = 5
    _effect_on_turn = gain_mana
