from typing import Type

from base_spell import  BaseSpell
from game_state_change import GameStateChange
from spell_type import SpellType


class GameState:
    def __init__(
            self,
            boss_hp: int = 51,
            boss_dmg: int = 9,
            player_mana: int = 500,
            player_hp: int = 50,
            player_armor: int = 0,
            mana_spent: int = 0,
            spells_cast: list[SpellType] = None,
            available_spells: list[Type[BaseSpell]] = None,
            active_spells: list[BaseSpell] = None,
            is_hard_mode: bool = False,
    ):
        self._player_mana = player_mana
        self._player_hp = player_hp
        self._player_armor = player_armor
        self._boss_hp = boss_hp
        self._boss_dmg = boss_dmg
        self._mana_spent = mana_spent
        self._is_hard_mode = is_hard_mode

        self._eot_events = []

        if spells_cast is None:
            self._spells_cast = []
        else:
            self._spells_cast = spells_cast

        if active_spells is None:
            self._active_spells = []
        else:
            self._active_spells = active_spells

        if available_spells is None:
            self._available_spells = []
        else:
            self._available_spells = available_spells

    @property
    def boss_hp(self):
        return self._boss_hp

    @property
    def mana_spent(self):
        return self._mana_spent

    @property
    def spells_cast(self):
        return [_.value for _ in self._spells_cast]

    def __lt__(self, other):
        if not isinstance(other, GameState):
            raise ValueError(f"Cannot compare {self.__class__} to {type(other)}")

        return (self.mana_spent, self.boss_hp) < (other.mana_spent, other.boss_hp)

    def apply_effect(self, change: GameStateChange | None):
        if change is None:
            return

        self._boss_hp += change.boss_hp_change
        self._player_hp += change.player_hp_change
        self._player_mana += change.player_mana_change
        self._player_armor += change.player_armor_change

    def apply_spells(self):
        new_active = []

        for spell in self._active_spells:
            spell.advance_turn()
            self.apply_effect(spell.effect_on_turn)

            if spell.turns_left > 0:
                new_active.append(spell.copy())
            else:
                self._eot_events.append(spell.effect_on_end)

        self._active_spells = new_active

    def apply_eot_effects(self):
        for effect in self._eot_events:
            self.apply_effect(effect)
        self._eot_events = []

    def boss_turn(self):
        self.apply_spells()

        if self._boss_hp <= 0:
            return True

        self._player_hp -= self._boss_dmg - self._player_armor

        if self._player_hp <= 0:
            return False

        return None

    def get_next_states(self):
        if self._is_hard_mode:
            self._player_hp -= 1

            if self._player_hp <= 0:
                return False, []

        self.apply_spells()

        if self._boss_hp <= 0:
            return True, None

        active_types = set(__.spell_type for __ in self._active_spells)
        allowed_spells =  [
            _ for _ in self._available_spells if _.spell_type not in active_types and _.cost <= self._player_mana
        ]

        next_states = []
        for spell_literal in allowed_spells:
            active_spells = [_.copy() for _ in self._active_spells]

            new_spell = spell_literal()
            if new_spell.turns_left > 0:
                active_spells.append(new_spell)

            new_state = GameState(
                boss_hp=self._boss_hp,
                boss_dmg=self._boss_dmg,
                player_mana=self._player_mana - new_spell.cost,
                player_hp=self._player_hp,
                mana_spent=self._mana_spent + new_spell.cost,
                player_armor=self._player_armor,
                spells_cast=self._spells_cast + [new_spell.spell_type],
                available_spells=self._available_spells,
                active_spells=active_spells,
                is_hard_mode=self._is_hard_mode,
            )
            new_state.apply_effect(new_spell.effect_on_cast)

            next_states.append(new_state)
        return False, next_states
