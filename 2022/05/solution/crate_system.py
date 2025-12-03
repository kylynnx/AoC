import re


class CrateSystem:
    def __init__(self, crate_string: str):
        crate_lines = crate_string.split('\n')
        count_crates = int(crate_lines.pop(-1)[-1])

        self._piles = []
        for _ in range(count_crates):
            self._piles.append([])

        for crate_line in crate_lines:
            current_start = 0
            current_pile = 0
            while current_start < len(crate_line):
                if (crate := crate_line[current_start:current_start + 3]) != '   ':
                    self._piles[current_pile].insert(0, crate[1])

                current_pile += 1
                current_start += 4

    @staticmethod
    def read_operation(operation: str):
        match = re.match(r'^move (\d{1,2}) from (\d) to (\d)$', operation)
        count_moved = int(match.group(1))
        from_pile = int(match.group(2)) - 1
        to_pile = int(match.group(3)) - 1

        return count_moved, from_pile, to_pile

    def perform_operation_9000(self, operation: str):
        count_moved, from_pile, to_pile = self.read_operation(operation)

        for _ in range(count_moved):
            self._piles[to_pile].append(self._piles[from_pile].pop(-1))

    def perform_operation_9001(self, operation: str):
        count_moved, from_pile, to_pile = self.read_operation(operation)

        moved_crates = self._piles[from_pile][-count_moved:]
        self._piles[from_pile] = self._piles[from_pile][:-count_moved]
        self._piles[to_pile] += moved_crates

    @property
    def top_crates(self):
        return ''.join(_[-1] for _ in self._piles)
