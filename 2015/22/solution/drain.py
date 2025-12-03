from base_spell import BaseSpell
from game_state_change import GameStateChange
from spell_type import SpellType


deal_two_heal_two = GameStateChange(boss_hp_change=-2, player_hp_change=2)

class Drain(BaseSpell):
    spell_type = SpellType.DRAIN
    cost = 73
    _effect_on_cast = deal_two_heal_two
