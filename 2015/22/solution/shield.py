from base_spell import BaseSpell
from game_state_change import GameStateChange
from spell_type import SpellType

increase_armor = GameStateChange(player_armor_change=7)
decrease_armor = GameStateChange(player_armor_change=-7)


class Shield(BaseSpell):
    spell_type = SpellType.SHIELD
    cost = 113
    _turns_active = 7
    _effect_on_cast = increase_armor
    _effect_on_end = decrease_armor
