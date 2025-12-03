import re
from collections import defaultdict
from math import gcd


class FireWallLayer:
    def __init__(self, depth: int, scan_range: int):
        self.depth = depth
        self.scan_range = scan_range

    def __str__(self):
        return f"Depth: {self.depth} - Range: {self.scan_range}"

    @property
    def severity(self) -> int:
        return self.depth * self.scan_range

    @classmethod
    def from_string(cls, layer_string: str) -> "FireWallLayer":
        match = re.match(r"^([0-9]+): ([0-9]+)$", layer_string)

        return cls(depth=int(match.group(1)), scan_range=int(match.group(2)))

    def scanner_position(self, time: int) -> int:
        return time % (2 * (self.scan_range - 1))


def find_delay(layers: list[FireWallLayer]) -> int:
    """
    From Part one we know, that the package reaches the layer at a given depth after exactly that many steps, and the
    scanner position has a periodicity in positions of `2 * (range - 1)` steps.

    If we delay the package this gives us that the condition for the scanner to be at the top position is:

    ```
    delay + depth = 0 mod 2 * (range - 1)
    ```

    which can be rewritten to

    ```
    delay = - depth mod 2 * (range - 1)
    ```

    In this first step we store all these remainder conditionals for all layers of the same range.
    """
    non_divisibility_requirements = defaultdict(list)
    for layer in layers:
        steps_to_round_trip = 2 * (layer.scan_range - 1)
        non_divisibility_requirements[steps_to_round_trip] += [(-layer.depth) % steps_to_round_trip]

    moduli = sorted(non_divisibility_requirements.keys())
    lcm = 1
    residues = [0]
    """
    Now for every scan range (represented as the moduli) we determine the least common multiple of it and all previous
    moduli.
    
    We then check every number for the non divisibility requirements. This can be done starting from the residues from
    the previous steps upto a maximum of the lcm as we are looking for a minimum. It is done in steps of the previous
    lcm to preserve the divisibility established in former steps. 
    
    The minimum of the residues in the end will give our result.
    """
    for modulus in moduli:
        divisor = gcd(modulus, lcm)
        previous_lcm = lcm
        lcm *= modulus // divisor

        # a = [1, 2]
        # b = [3, 4]
        # sum([a, b], []) -> [1, 2, 3, 4]
        residues = [
            residue for residue in
            sum([list(range(_, lcm, previous_lcm)) for _ in residues], [])
            if residue % modulus not in non_divisibility_requirements[modulus]
        ]

    return sorted(residues)[0]


def main(filename: str):
    with open(filename) as file:
        layers = [FireWallLayer.from_string(_.strip()) for _ in file.readlines()]

    caught_layers = [_ for _ in layers if _.scanner_position(_.depth) == 0]
    total_severity = sum(_.severity for _ in caught_layers)
    print(f"The total severity of the trip is {total_severity}.")

    delay = find_delay(layers)
    print(f"The minimum delay not to be caught is {delay}.")


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
