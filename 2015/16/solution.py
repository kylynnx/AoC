import re


class Aunt:
    _attributes = [
        "children", "cats", "samoyeds", "pomeranians", "akitas", "vizslas", "goldfish", "trees", "cars", "perfumes"
    ]

    _more_than = ["cats", "trees"]
    _less_than = ["pomeranians", "goldfish"]

    def __init__(self, aunt_str: str):
        self.__setattr__("_id", self._get(name="Sue ", source=aunt_str))
        for attr in self._attributes:
            self.__setattr__(
                f"_{attr}", self._get(name=f".+{attr}: ", source=aunt_str)
            )

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except:
            return self.__getattribute__(f"_{item}")

    def __eq__(self, other):
        for attr in self._attributes:
            self_attr = self.__getattribute__(attr)
            other_attr = getattr(other, attr)

            if self_attr is None or other_attr is None:
                continue

            if self_attr != other_attr:
                return False

        return True

    def range_match(self, other):
        for attr in self._attributes:
            self_attr = self.__getattribute__(attr)
            other_attr = getattr(other, attr)

            if self_attr is None or other_attr is None:
                continue

            if (
                (attr in self._less_than and other_attr <= self_attr)
                or (attr in self._more_than and other_attr >= self_attr)
                or (
                    attr not in self._less_than
                    and attr not in self._more_than
                    and self_attr != other_attr
                )
            ):
                return False

        return True

    @staticmethod
    def _get(name: str, source: str):
        pattern = fr"{name}([0-9]+)(.+)?"
        match = re.match(pattern, source)

        if match:
            return int(match.group(1))

        return None


def main(filename: str):
    with open(filename) as f:
        aunts = [Aunt(_) for _ in f.readlines()]

    target_aunt = Aunt(
        "Sue 501: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, goldfish: 5, trees: 3, "
        "cars: 2, perfumes: 1"
    )

    match = None

    for aunt in aunts:
        if aunt == target_aunt:
            match = aunt
            break

    print(match.id)

    match = None

    for aunt in aunts:
        if aunt.range_match(target_aunt):
            match = aunt
            break

    print(match.id)


if __name__ == '__main__':
    main("input.txt")
