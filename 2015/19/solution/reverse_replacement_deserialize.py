import re

from reverse_replacement import ReverseReplacement


def deserialize(replacement_strings: list[str]):
    final_replacements = []
    intermediate_replacements = []
    for replacement_string in replacement_strings:
        match = re.match(r"([A-Za-z]+) => ([A-Za-z]+)", replacement_string)

        if match.group(1) == "e":
            final_replacements.append(ReverseReplacement(source=match.group(2), target=match.group(1)))
        else:
            intermediate_replacements.append(ReverseReplacement(source=match.group(2), target=match.group(1)))

    return intermediate_replacements, final_replacements
