import re
from abc import ABC
from enum import Enum
from typing import Set, Type, Dict


JOKER_NAME = 'J'


class CardSorter:
    _card_ranks = {
        'A': 12,
        'K': 11,
        'Q': 10,
        'J': 9,
        'T': 8,
        '9': 7,
        '8': 6,
        '7': 5,
        '6': 4,
        '5': 3,
        '4': 2,
        '3': 1,
        '2': 0
    }

    @classmethod
    def less_than(cls, left, right):
        return cls._card_ranks[left] < cls._card_ranks[right]

    @classmethod
    def less_than_or_equal(cls, left, right):
        return cls._card_ranks[left] <= cls._card_ranks[right]

    @classmethod
    def greater_than(cls, left, right):
        return cls._card_ranks[left] > cls._card_ranks[right]

    @classmethod
    def greater_than_or_equal(cls, left, right):
        return cls._card_ranks[left] >= cls._card_ranks[right]


class HandType(Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


class Hand(ABC):
    _hand_type: HandType = None
    _card_sorter: Type[CardSorter] = CardSorter

    def __init__(self, bid: int, cards_string: str):
        self._bid = bid
        self._cards = cards_string

    @property
    def bid(self):
        return self._bid

    @property
    def cards(self):
        return self._cards

    @property
    def hand_type(self):
        return self._hand_type

    def __str__(self):
        return f'Type {HandType(self._hand_type.value).name}, Cards: {self._cards}, Bid: {self._bid}\n'

    def __eq__(self, other):
        if not isinstance(other, Hand):
            raise NotImplemented

        return self._hand_type == other.hand_type and self._cards == other.cards

    def __lt__(self, other):
        if not isinstance(other, Hand):
            raise NotImplemented

        if self._hand_type.value < other.hand_type.value:
            return True

        if self._hand_type.value == other.hand_type.value:
            for self_card, other_card in zip(self._cards, other.cards):
                if self_card == other_card:
                    continue
                return self._card_sorter.less_than(self_card, other_card)
            return True  # choice: not explicitly stated in exercise!

        return False

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return not self < other and not self == other

    def __le__(self, other):
        return self < other or self == other


class FiveOfAKindHand(Hand):
    _hand_type = HandType.FIVE_OF_A_KIND


class FourOfAKindHand(Hand):
    _hand_type = HandType.FOUR_OF_A_KIND
    pass


class FullHouseHand(Hand):
    _hand_type = HandType.FULL_HOUSE
    pass


class ThreeOfAKindHand(Hand):
    _hand_type = HandType.THREE_OF_A_KIND
    pass


class TwoPairHand(Hand):
    _hand_type = HandType.TWO_PAIR
    pass


class OnePairHand(Hand):
    _hand_type = HandType.ONE_PAIR
    pass


class HighCardHand(Hand):
    _hand_type = HandType.HIGH_CARD
    pass


class HandFactory:
    @staticmethod
    def produce(bid_string: str, cards_string: str) -> Hand:
        cards_set = {_ for _ in cards_string}
        bid = int(bid_string)

        match len(cards_set):
            case 1:
                return FiveOfAKindHand(bid=bid, cards_string=cards_string)
            case 2:
                return HandFactory._two_unique_cards_produce(bid=bid, cards_string=cards_string, cards_set=cards_set)
            case 3:
                return HandFactory._three_unique_cards_produce(bid=bid, cards_string=cards_string, cards_set=cards_set)
            case 4:
                return OnePairHand(bid=bid, cards_string=cards_string)
            case 5:
                return HighCardHand(bid=bid, cards_string=cards_string)
            case _:
                raise ValueError('Unknown cards string')

    @staticmethod
    def _two_unique_cards_produce(bid: int, cards_string: str, cards_set: Set[str]) -> Hand:
        _relative_frequencies = {cards_string.count(_) for _ in cards_set}

        if _relative_frequencies == {1, 4}:
            return FourOfAKindHand(bid=bid, cards_string=cards_string)
        elif _relative_frequencies == {2, 3}:
            return FullHouseHand(bid=bid, cards_string=cards_string)

        raise ValueError('Forbidden combination')

    @staticmethod
    def _three_unique_cards_produce(bid: int, cards_string: str, cards_set: Set[str]) -> Hand:
        _relative_frequencies = {cards_string.count(_) for _ in cards_set}

        # using sets reduces the actual frequencies down to two numbers
        if _relative_frequencies == {1, 3}:    # actual frequencies: (1,1,3)
            return ThreeOfAKindHand(bid=bid, cards_string=cards_string)
        elif _relative_frequencies == {1, 2}:  # actual frequencies: (1, 2, 2)
            return TwoPairHand(bid=bid, cards_string=cards_string)

        raise ValueError('Forbidden combination')


class HandCollection:
    def __init__(self, factory: Type[HandFactory], filename: str):
        with open(filename, 'r') as _f:
            _hand_bid_strings = _f.readlines()

        self._hands = []
        for hand_bid in _hand_bid_strings:
            match = re.match(r'([2-9TJQKA]{5}) ([0-9]+)', hand_bid)
            self._hands.append(factory.produce(bid_string=match.group(2), cards_string=match.group(1)))

        self._sorted_hands = None
        self._winnings = None

    @property
    def hands(self):
        if not self._sorted_hands:
            self._sorted_hands = sorted(self._hands)

        return self._sorted_hands

    @property
    def winnings(self):
        if not self._winnings:
            _hands = self.hands
            self._winnings = sum([(_hands.index(_) + 1) * _.bid for _ in _hands])

        return self._winnings


class JokerCardSorter(CardSorter):
    _card_ranks = {
        'A': 12,
        'K': 11,
        'Q': 10,
        'T': 9,
        '9': 8,
        '8': 7,
        '7': 6,
        '6': 5,
        '5': 4,
        '4': 3,
        '3': 2,
        '2': 1,
        'J': 0,
    }


class JokerHand(Hand):
    _card_sorter = JokerCardSorter


class FiveOfAKindJokerHand(JokerHand):
    _hand_type = HandType.FIVE_OF_A_KIND


class FourOfAKindJokerHand(JokerHand):
    _hand_type = HandType.FOUR_OF_A_KIND
    pass


class FullHouseJokerHand(JokerHand):
    _hand_type = HandType.FULL_HOUSE
    pass


class ThreeOfAKindJokerHand(JokerHand):
    _hand_type = HandType.THREE_OF_A_KIND
    pass


class TwoPairJokerHand(JokerHand):
    _hand_type = HandType.TWO_PAIR
    pass


class OnePairJokerHand(JokerHand):
    _hand_type = HandType.ONE_PAIR
    pass


class HighCardJokerHand(JokerHand):
    _hand_type = HandType.HIGH_CARD
    pass


class JokerHandFactory(HandFactory):
    _type_map: Dict[HandType, Type[JokerHand]] = {
        HandType.FIVE_OF_A_KIND: FiveOfAKindJokerHand,
        HandType.FOUR_OF_A_KIND: FourOfAKindJokerHand,
        HandType.FULL_HOUSE: FullHouseJokerHand,
        HandType.THREE_OF_A_KIND: ThreeOfAKindJokerHand,
        HandType.TWO_PAIR: TwoPairJokerHand,
        HandType.ONE_PAIR: OnePairJokerHand,
        HandType.HIGH_CARD: HighCardJokerHand
    }

    @staticmethod
    def produce(bid_string: str, cards_string: str) -> JokerHand:
        if JOKER_NAME not in cards_string:
            return JokerHandFactory._retype(HandFactory.produce(bid_string=bid_string, cards_string=cards_string))

        bid = int(bid_string)
        non_joker_cards = {_ for _ in cards_string if _ != JOKER_NAME}
        unique_non_joker_cards = len(non_joker_cards)
        match cards_string.count(JOKER_NAME):
            case 1:
                return JokerHandFactory._one_joker_produce(
                    unique_non_joker_cards=unique_non_joker_cards,
                    non_joker_cards=non_joker_cards,
                    bid=bid,
                    cards_string=cards_string
                )
            case 2:
                return JokerHandFactory._two_joker_produce(
                    unique_non_joker_cards=unique_non_joker_cards, bid=bid, cards_string=cards_string
                )
            case 3:
                return JokerHandFactory._three_joker_produce(
                    unique_non_joker_cards=unique_non_joker_cards, bid=bid, cards_string=cards_string
                )
            case _:
                return FiveOfAKindJokerHand(bid=bid, cards_string=cards_string)

    @staticmethod
    def _retype(hand: Hand) -> JokerHand:
        return JokerHandFactory._type_map[hand.hand_type](bid=hand.bid, cards_string=hand.cards)

    @staticmethod
    def _one_joker_produce(
            unique_non_joker_cards: int, non_joker_cards: Set[str], bid: int, cards_string: str) -> JokerHand:
        match unique_non_joker_cards:
            case 1:
                return FiveOfAKindJokerHand(bid=bid, cards_string=cards_string)
            case 2:
                return JokerHandFactory._one_joker_two_unique_produce(
                    non_joker_cards=non_joker_cards, bid=bid, cards_string=cards_string
                )
            case 3:
                return ThreeOfAKindJokerHand(bid=bid, cards_string=cards_string)
            case 4:
                return OnePairJokerHand(bid=bid, cards_string=cards_string)

    @staticmethod
    def _one_joker_two_unique_produce(non_joker_cards: Set[str], bid: int, cards_string: str) -> JokerHand:
        _counts = {cards_string.count(_) for _ in non_joker_cards}

        if _counts == {1, 3}:
            return FourOfAKindJokerHand(bid=bid, cards_string=cards_string)
        elif _counts == {2}:  # actual (2, 2)
            return FullHouseJokerHand(bid=bid, cards_string=cards_string)
        else:
            raise ValueError(f'Invalid 1 Joker, 2 unique other combination: {cards_string}')

    @staticmethod
    def _two_joker_produce(unique_non_joker_cards: int, bid: int, cards_string: str) -> JokerHand:
        match unique_non_joker_cards:
            case 1:
                return FiveOfAKindJokerHand(bid=bid, cards_string=cards_string)
            case 2:
                return FourOfAKindJokerHand(bid=bid, cards_string=cards_string)
            case 3:
                return ThreeOfAKindJokerHand(bid=bid, cards_string=cards_string)

    @staticmethod
    def _three_joker_produce(unique_non_joker_cards: int, bid: int, cards_string: str) -> JokerHand:
        match unique_non_joker_cards:
            case 1:
                return FiveOfAKindJokerHand(bid=bid, cards_string=cards_string)
            case 2:
                return FourOfAKindJokerHand(bid=bid, cards_string=cards_string)


def main(filename: str):
    collection = HandCollection(factory=HandFactory, filename=filename)
    print(collection.winnings)

    joker_collection = HandCollection(factory=JokerHandFactory, filename=filename)
    print(joker_collection.winnings)


if __name__ == '__main__':
    main('./input.txt')
