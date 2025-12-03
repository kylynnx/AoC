import re

from replacement_lookup import ReplacementLookup


class ReplacementFactory:
    @staticmethod
    def generate(replacement_strings: list[str]) -> ReplacementLookup:
        lookup = ReplacementLookup()

        for replacement_string in replacement_strings:
            match  = re.match(r"([A-Za-z]+) => ([A-Za-z]+)", replacement_string)

            lookup.add_replacement(target=match.group(1), replacement=match.group(2))

        return lookup
