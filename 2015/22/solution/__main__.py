from way_finder import find_least_mana_win
from game_state import GameState
from drain import Drain
from magic_missile import MagicMissile
from poison import Poison
from recharge import Recharge
from shield import Shield

def main(boss_hp: int, boss_dmg: int, player_hp: int, player_mana: int, is_hard_mode: bool = False):
    available_spells = [Drain, MagicMissile, Poison, Recharge, Shield]
    initial_state = GameState(
        boss_hp=boss_hp,
        boss_dmg=boss_dmg,
        player_hp=player_hp,
        player_mana=player_mana,
        available_spells=available_spells,
        is_hard_mode=is_hard_mode,
    )
    least_mana_win = find_least_mana_win(initial_state)
    print(least_mana_win.mana_spent)
    print(least_mana_win.spells_cast)


if __name__ == "__main__":
    main(boss_hp=13, boss_dmg=8, player_hp=10, player_mana=250)  # P, MM
    main(boss_hp=14, boss_dmg=8, player_hp=10, player_mana=250)  # R, S, D, P, MM
    main(boss_hp=51, boss_dmg=9, player_hp=50, player_mana=500)  # P, R, S, P, MM, MM, MM, MM
    main(boss_hp=51, boss_dmg=9, player_hp=50, player_mana=500, is_hard_mode=True)
