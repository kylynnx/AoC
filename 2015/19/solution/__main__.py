from analyzer import MoleculeAnalyzer
from molecule_factory import MoleculeFactory
from replacement_factory import ReplacementFactory
from reverse_replacement_deserialize import deserialize


def calibrate(replacement_strings: list[str], medicine: str):
    replacement_lookup = ReplacementFactory.generate(replacement_strings=replacement_strings)
    molecule_factory = MoleculeFactory(base_molecule=medicine, replacements=replacement_lookup)
    molecule_factory.produce_molecules()
    print(molecule_factory.molecule_count)


def analyze(replacement_strings: list[str], medicine: str):
    intermediates, finalizers = deserialize(replacement_strings=replacement_strings)
    molecule_analyzer = MoleculeAnalyzer(molecule=medicine, intermediates=intermediates, finalizers=finalizers)
    steps = molecule_analyzer.analyze()
    print(steps)


def main(filename: str):
    with open(filename) as f:
        replacements, medicine = f.read().split("\n\n")

    replacement_strings = [_.strip("\n") for _ in replacements.split("\n")]
    medicine = medicine.strip("\n")

    calibrate(replacement_strings, medicine)
    analyze(replacement_strings, medicine)


if __name__ == "__main__":
    main("../input.txt")
