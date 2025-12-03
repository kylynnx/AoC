from collections import defaultdict


class ReplacementLookup:
    def __init__(self):
        self._replacements = defaultdict(set)

    def add_replacement(self, target: str, replacement: str):
        self._replacements[target].add(replacement)

    def get_replacements(self, target: str) -> set[str]:
        return self._replacements[target]

    def __iter__(self):
        for target, replacements in self._replacements.items():
            for replacement in replacements:
                yield target, replacement
