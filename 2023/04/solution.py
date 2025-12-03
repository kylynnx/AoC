import math
import re
from pprint import pprint
from typing import List


def get_numbers_from_string(number_string: str) -> List[int]:
    return [int(_) for _ in re.findall(r'([0-9]+)', number_string)]


class Card:
    def __init__(self, card_string: str):
        match = re.match(r'Card\s+([0-9]{1,3}):\s+([0-9\s]+)\| ([0-9\s]+)$', card_string)
        self._id = int(match.group(1))
        self._winning_numbers = get_numbers_from_string(match.group(2))
        self._having_numbers = get_numbers_from_string(match.group(3))

        self._winners = len([_ for _ in self._having_numbers if _ in self._winning_numbers])

        self._points = None
        self._is_winner = self._winners > 0

    @property
    def id(self):
        return self._id

    @property
    def winners(self):
        return self._winners

    @property
    def points(self):
        if self._points is None:
            if self._winners > 0:
                self._points = int(math.pow(2, self._winners - 1))
            else:
                self._points = 0
        return self._points


def main(filename: str):
    with open(filename, 'r') as _f:
        collection = _f.readlines()

    cards = []
    for card_string in collection:
        cards.append(Card(card_string))

    points = [_.points for _ in cards]

    print(sum(points))

    point_lookup = {}

    cards.reverse()
    max_id = len(cards) + 1

    for card in cards:
        _points = 1

        won_card_range = card.winners
        if won_card_range:
            for won_card in range(card.id + 1, min(max_id, card.id + won_card_range + 1)):
                _points += point_lookup[won_card]

        point_lookup[card.id] = _points

    print(point_lookup)
    print(sum(point_lookup.values()))


if __name__ == '__main__':
    main('./input.txt')
