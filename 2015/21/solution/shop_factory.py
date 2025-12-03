import re

from equipment import Equipment
from shop import Shop


class ShopFactory:
    @staticmethod
    def open_shop(armors_file: str, rings_file: str, weapons_file: str):
        armors = ShopFactory.load_equipment_file(armors_file)
        armors.append(Equipment(armor=0, damage=0, cost=0))  # not wearing armor is a choice
        rings = ShopFactory.load_equipment_file(rings_file)
        rings.append(Equipment(armor=0, damage=0, cost=0))  # wearing just one ring is allowed
        rings.append(Equipment(armor=0, damage=0, cost=0))  # or not wearing rings at all
        weapons = ShopFactory.load_equipment_file(weapons_file)

        return Shop(
            armors=armors,
            rings=rings,
            weapons=weapons,
        )

    @staticmethod
    def _deserialize_equipment_list(equipment_strings: list[str]) -> list[Equipment]:
        result = []
        for equipment_string in equipment_strings:
            match = re.match(r"^[A-Za-z\s+1-3]+\s(\d+)\s+(\d)\s+(\d)$", equipment_string)
            result.append(
                Equipment(
                    cost=int(match.group(1)),
                    damage=int(match.group(2)),
                    armor=int(match.group(3)),
                )
            )
        return result

    @staticmethod
    def load_equipment_file(equipment_file: str) -> list[Equipment]:
        with open(equipment_file) as f:
            equipment_strings = f.readlines()[1:]

        return ShopFactory._deserialize_equipment_list(equipment_strings=equipment_strings)
