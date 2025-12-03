import re


def deserialize_map_string(map_str: str) -> (str, str, int):
    match = re.match("([A-Za-z]+) to ([A-Za-z]+) = ([0-9]+)", map_str)

    return match.group(1), match.group(2), int(match.group(3))
