from base_spell import BaseSpell
from game_state_change import GameStateChange
from spell_type import SpellType

deal_three_damage = GameStateChange(boss_hp_change=-3)


class Poison(BaseSpell):
    spell_type = SpellType.POISON
    cost = 173
    _turns_active = 6
    _effect_on_turn = deal_three_damage
