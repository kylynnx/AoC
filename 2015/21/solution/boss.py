import re

from combatant import Combatant


class Boss(Combatant):
    def __init__(self, filename: str):
        super().__init__()

        with open(filename) as f:
            hp_string, dmg_string, armor_string = f.readlines()

        hp_match = re.match("Hit Points: ([0-9]+)", hp_string)
        self._hit_points = int(hp_match.group(1))

        dmg_match = re.match("Damage: ([0-9]+)", dmg_string)
        self._damage = int(dmg_match.group(1))

        armor_match = re.match("Armor: ([0-9]+)", armor_string)
        self._armor = int(armor_match.group(1))
