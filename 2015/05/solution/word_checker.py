from typing import Type

from rules import Rule


class WordChecker:
    def __init__(self, rules: list[Type[Rule]]):
        self._rules = rules

    def check(self, words: list[str]):
        nice_words = 0

        for word in words:
            nice_words += self._check_word(word)

        return nice_words

    def _check_word(self, word: str):
        for rule in self._rules:
            if not rule.check(word):
                return False

        return True
