import re
from abc import abstractmethod


class Rule:
    @classmethod
    @abstractmethod
    def check(cls, word: str) -> bool:
        pass


class ThreeVowelRule(Rule):
    _vowels = "aeiou"

    @classmethod
    def check(cls, word: str) -> bool:
        vowel_count = 0
        for vowel in cls._vowels:
            vowel_count += word.count(vowel)

        return vowel_count >= 3


class DoubleLetterRule(Rule):
    @classmethod
    def check(cls, word: str) -> bool:
        match = re.search(r"([a-z])\1", word)

        return bool(match)


class NaughtyStringRule(Rule):
    _naughty_strings = ["ab", "cd", "pq", "xy"]

    @classmethod
    def check(cls, word: str) -> bool:
        if any(_ in word for _ in cls._naughty_strings):
            return False

        return True


class RepeatingDoubleLetterRule(Rule):
    @classmethod
    def check(cls, word: str) -> bool:
        match = re.search(r"([a-z][a-z])([a-z]+)?\1", word)

        return bool(match)


class RepeatingSingleLetterRule(Rule):
    @classmethod
    def check(cls, word: str) -> bool:
        match = re.search(r"([a-z])[a-z]\1", word)

        return bool(match)
