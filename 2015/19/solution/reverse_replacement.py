class ReverseReplacement:
    def __init__(self, source: str, target: str):
        self._source = source
        self._target = target

    def replace(self, molecule: str) -> (str, int):
        replacements = 0
        while (start := molecule.find(self._source)) >= 0:
            molecule = molecule[:start] + self._target + molecule[start + len(self._source):]
            replacements += 1

        return molecule, replacements
