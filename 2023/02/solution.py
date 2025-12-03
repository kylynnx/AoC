import re

from typing import List


class ColorCombination:
    def __init__(self, red: int, green: int, blue: int):
        self._red = red
        self._green = green
        self._blue = blue

    @property
    def red(self) -> int:
        return self._red

    @property
    def green(self) -> int:
        return self._green

    @property
    def blue(self) -> int:
        return self._blue

    def __le__(self, other: 'ColorCombination') -> bool:
        if not isinstance(other, ColorCombination):
            raise NotImplemented
        return (self._red <= other.red) and (self._green <= other.green) and (self._blue <= other.blue)


class Game:
    def __init__(self, game_id: int, legs: List[ColorCombination]):
        self._game_id = game_id
        self._legs = legs
        self._power = None

    @property
    def game_id(self) -> int:
        return self._game_id

    def __le__(self, other: ColorCombination) -> bool:
        if not isinstance(other, ColorCombination):
            raise NotImplemented

        return all([_ <= other for _ in self._legs])

    @property
    def power(self):
        if not self._power:
            min_red = max([_.red for _ in self._legs])
            min_blue = max([_.blue for _ in self._legs])
            min_green = max([_.green for _ in self._legs])

            self._power = min_red * min_blue * min_green

        return self._power


def read_input(filename: str) -> List[str]:
    with open(filename, 'r') as _f:
        return _f.readlines()


def find_color(leg_string: str, color: str) -> int:
    match = re.match(fr'(\d\d?) {color}', leg_string)
    if match:
        return int(match.group(1))
    return 0


def read_leg(leg_string: str) -> ColorCombination:
    parts = leg_string.split(', ')
    red = sum([find_color(_, 'red') for _ in parts])
    green = sum([find_color(_, 'green') for _ in parts])
    blue = sum([find_color(_, 'blue') for _ in parts])

    return ColorCombination(red=red, green=green, blue=blue)


def read_game(game_string: str) -> Game:
    match = re.match(r'^Game (\d{1,3}): (.*)$', game_string)
    game_id = int(match.group(1))
    combined_leg_strings = match.group(2).split("; ")
    legs = [read_leg(_) for _ in combined_leg_strings]

    return Game(game_id=game_id, legs=legs)


def main(filename: str, red_count: int, green_count: int, blue_count: int):
    bag_content = ColorCombination(red=red_count, green=green_count, blue=blue_count)
    game_strings = read_input(filename)
    games = [read_game(_) for _ in game_strings]

    possible_games = [_.game_id for _ in games if _ <= bag_content]

    print(sum(possible_games))

    powers = [_.power for _ in games]
    print(sum(powers))


if __name__ == '__main__':
    main('./input.txt', red_count=12, green_count=13, blue_count=14)
