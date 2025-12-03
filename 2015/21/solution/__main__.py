from boss import Boss
from player import Player
from shop_factory import ShopFactory


def main(armors_file: str, weapons_file: str, rings_file: str, boss_file: str):
    boss = Boss(boss_file)
    shop = ShopFactory.open_shop(armors_file=armors_file, weapons_file=weapons_file, rings_file=rings_file)
    player = Player()
    loadouts = [_ for _ in shop]
    loadouts.sort(key=lambda x: x.cost)

    for loadout in loadouts:
        player.don_loadout(loadout)
        if player.beats(boss):
            print(loadout.cost)
            break

    loadouts.reverse()
    for loadout in loadouts:
        player.don_loadout(loadout)
        if not player.beats(boss):
            print(loadout.cost)
            break


if __name__ == "__main__":
    main(
        armors_file="../armors.txt",
        weapons_file="../weapons.txt",
        rings_file="../rings.txt",
        boss_file="../boss.txt",
    )
