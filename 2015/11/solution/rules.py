import string
from abc import abstractmethod


class Rule:
    @classmethod
    @abstractmethod
    def check(cls, word: str) -> bool:
        pass


class ForbiddenLetterRule(Rule):
    _forbidden_letters = {"i", "o", "l"}

    @classmethod
    def check(cls, word: str) -> bool:
        return not any(_ in word for _ in cls._forbidden_letters)


class LetterPairRule(Rule):
    _letters = string.ascii_lowercase

    @classmethod
    def check(cls, word: str) -> bool:
        return sum(word.count(f"{_}{_}") for _ in cls._letters) >= 2


class IncreasingLetterStraightRule(Rule):
    _length = 3
    _letters = string.ascii_lowercase

    @classmethod
    def check(cls, word: str) -> bool:
        return any(
            cls._letters[_: _ + cls._length] in word
            for _ in range(len(cls._letters) - cls._length + 1)
        )
