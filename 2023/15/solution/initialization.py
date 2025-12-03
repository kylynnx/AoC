import re
from enum import Enum
from typing import List

from elf_hash import elf_hash_function


class Operation(Enum):
    REMOVE = '-'
    ADD = '='


class Lens:
    def __init__(self, label: str, focal_length: int):
        self._label = label
        self._focal_length = focal_length

    @property
    def label(self):
        return self._label

    @property
    def focal_length(self):
        return self._focal_length

    @focal_length.setter
    def focal_length(self, value: int):
        self._focal_length = value


class HashMap:
    def __init__(self, modulus: int):
        self._lenses: List[List[Lens]] = []
        for _ in range(modulus):
            self._lenses.append([])
        self._modulus = modulus
        self._power = None

    def perform_operation(self, operation_string: str):
        if Operation.ADD.value in operation_string:
            self._perform_add(operation_string)
        else:
            self._perform_remove(operation_string)

    def _perform_add(self, operation_string: str):
        match = re.match(r'(.+)=(\d+)', operation_string)
        label = match.group(1)
        box_number = elf_hash_function(label, modulus=self._modulus)
        focal = int(match.group(2))

        lenses = [_ for _ in self._lenses[box_number] if _.label == label]
        if lenses:
            for lens in lenses:
                lens.focal_length = focal
        else:
            self._lenses[box_number].append(Lens(label=label, focal_length=focal))

    def _perform_remove(self, operation_string: str):
        match = re.match(r'(.+)-', operation_string)
        label = match.group(1)
        box_number = elf_hash_function(label, modulus=self._modulus)
        lenses = [self._lenses[box_number].index(_) for _ in self._lenses[box_number] if _.label == label]
        if lenses:
            lenses.reverse()
            for to_pop in lenses:
                self._lenses[box_number].pop(to_pop)

    @property
    def focussing_power(self):
        if self._power is None:
            _power = 0
            _box_number = 0
            for box in self._lenses:
                _box_number += 1
                _lens_number = 0
                for lens in box:
                    _lens_number += 1
                    _power += _box_number * _lens_number * lens.focal_length
            self._power = _power
        return self._power
