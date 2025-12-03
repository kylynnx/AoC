import re
from copy import copy
from itertools import combinations

type floor_combinations = list[tuple[set[str], set[str]]]


def check_floor_safe(generators: set[str], microchips: set[str]) -> bool:
    solo_microchips = microchips - generators

    return not (solo_microchips and generators)


class Floor:
    def __init__(self, generators: set[str], microchips: set[str]):
        self.generators = generators
        self.microchips = microchips

    def __str__(self):
        floor = (" ".join(f"{_[0].upper()}G" for _ in self.generators) + " " ) if self.generators else ""
        floor += " ".join(f"{_[0].upper()}M" for _ in self.microchips) if self.microchips else ""
        return floor

    @property
    def is_empty(self):
        return not (self.generators or self.microchips)

    def copy(self) -> "Floor":
        return Floor(generators=copy(self.generators), microchips=copy(self.microchips))

    @property
    def pair_count(self) -> int:
        return len(self.microchips.intersection(self.generators))

    @property
    def single_microchips(self):
        return self.microchips - self.generators

    def combinations(self) -> floor_combinations:
        safe_combinations: floor_combinations = list()

        # one generator moving
        for generator in self.generators:
            if check_floor_safe(set(_ for _ in self.generators if _ != generator), self.microchips):
                safe_combinations.append(({generator,}, set()))
            # add generator microchip combination if present
            if generator in self.microchips:
                safe_combinations.append(({generator,}, {generator,}))

        # two generators moving
        for generators in combinations(self.generators, 2):
            moving_generators = set(generators)
            if check_floor_safe(self.generators - moving_generators, self.microchips):
                safe_combinations.append((moving_generators, set()))

        # one microchip moving
        for microchip in self.microchips:
            if check_floor_safe(self.generators, set(_ for _ in self.microchips if _ != microchip)):
                safe_combinations.append((set(), {microchip,}))

        # two microchips moving
        for microchips in combinations(self.microchips, 2):
            moving_microchips = set(microchips)
            if check_floor_safe(self.generators, self.microchips - moving_microchips):
                safe_combinations.append((set(), moving_microchips))

        return safe_combinations


class BuildingState:
    def __init__(self, floors: list[Floor], elevator_floor: int, minimal_floor: int, moves: int):
        self.floors = floors
        self.elevator_floor = elevator_floor
        self.minimal_floor = minimal_floor
        self._moves  = moves

    @property
    def moves(self) -> int:
        return self._moves

    @property
    def assembled(self):
        return [_.is_empty for _ in self.floors] == [True, True, True, False]

    @staticmethod
    def from_file(filename: str) -> "BuildingState":
        with open(filename) as f:
            floor_descriptions = f.readlines()

        floors = []

        for index, floor in enumerate(floor_descriptions):
            microchips = set(re.findall("([a-z]+)-compatible microchip", floor))
            generators = set(re.findall("([a-z]+) generator", floor))
            floors.append(Floor(generators=generators, microchips=microchips))

        return BuildingState(floors, elevator_floor=0, minimal_floor=0, moves=0)

    def __str__(self):
        building = ""
        for floor_id, floor in enumerate(self.floors):
            building = f"F{floor_id + 1}{" E" if floor_id == self.elevator_floor else "  "} {floor}\n" + building

        return building

    @property
    def id(self):
        pairs = tuple(_.pair_count for _ in self.floors)
        brackets = []
        for idx, floor in enumerate(self.floors):
            local_brackets = []
            for chip in floor.single_microchips:
                local_brackets.append((idx, [chip in _.generators for _ in self.floors].index(True)))
            brackets += sorted(local_brackets)
        return self.elevator_floor, pairs, tuple(_ for _ in brackets)
