from base_spell import BaseSpell
from game_state_change import GameStateChange
from spell_type import SpellType


deal_four_damage = GameStateChange(boss_hp_change=-4)


class MagicMissile(BaseSpell):
    spell_type = SpellType.MAGIC_MISSILE
    cost = 53
    _effect_on_cast = deal_four_damage
