import re

from replacement_lookup import ReplacementLookup


class MoleculeFactory:
    def __init__(self, base_molecule: str, replacements: ReplacementLookup):
        self._base_molecule = base_molecule
        self._replacements = replacements
        self._produced_molecules = set()

    @property
    def molecule_count(self):
        return len(self._produced_molecules)

    def produce_molecules(self):
        for target, replacement in self._replacements:
            for match in re.finditer(target, self._base_molecule):
                self._produced_molecules.add(
                    self._base_molecule[:match.start()] + replacement + self._base_molecule[match.end():]
                )