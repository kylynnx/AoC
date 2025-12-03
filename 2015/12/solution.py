import json
import re


def part_one(filename: str) -> int:
    with open(filename) as f:
        content = f.read()

    matches = re.findall(r"-?[0-9]+", content)

    return sum(int(_) for _ in matches)


def get_sum(content: int | list | dict) -> int:
    if isinstance(content, int):
        return content

    if isinstance(content, list):
        return sum(get_sum(_) for _ in content)

    if isinstance(content, dict):
        if "red" in content.values():
            return 0

        return sum(get_sum(_) for _ in content.values())

    return 0


def part_two(filename: str) -> int:
    with open(filename) as f:
        content = json.load(f)

    return get_sum(content)


def main(filename: str):
    print(part_one(filename))
    print(part_two(filename))


if __name__ == '__main__':
    main("input.txt")
