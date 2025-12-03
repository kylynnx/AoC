from reverse_replacement import ReverseReplacement

REPL_LIST = list[ReverseReplacement]


class MoleculeAnalyzer:
    def __init__(self, molecule: str, intermediates: REPL_LIST, finalizers: REPL_LIST):
        self._molecule = molecule
        self._intermediates = intermediates
        self._finalizers = finalizers

    def analyze(self) -> int:
        previous_steps = -1
        steps = 0
        while (steps - previous_steps) > 0:
            previous_steps = steps
            for intermediate_replacement in self._intermediates:
                self._molecule, delta = intermediate_replacement.replace(self._molecule)
                steps += delta

        for finalizer in self._finalizers:
            self._molecule, delta = finalizer.replace(self._molecule)
            steps += delta
        return steps
