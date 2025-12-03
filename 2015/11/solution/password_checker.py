from typing import Type

from rules import Rule


class PasswordChecker:
    def __init__(self, rules: list[Type[Rule]]):
        self._rules = rules

    def check(self, password: str) -> bool:
        for rule in self._rules:
            if not rule.check(password):
                return False

        return True
