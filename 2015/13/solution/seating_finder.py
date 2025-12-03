from abc import abstractmethod
from itertools import permutations

from happiness_map import HappinessMap


class SeatingFinder:
    def __init__(self, starting_happiness):
        self._starting_happiness = starting_happiness
        self._optimal_happiness = starting_happiness

    @property
    def optimal_happiness(self):
        return self._optimal_happiness

    def find_seating(self, happiness_map: HappinessMap):
        head_count = len(happiness_map.people)

        for seating in permutations(happiness_map.people):
            current_happiness = 0
            for i in range(head_count):
                current_happiness += happiness_map.get_happiness_change(seating[i], seating[(i + 1) % head_count])
                current_happiness += happiness_map.get_happiness_change(seating[i], seating[(i - 1) % head_count])

            if self._accept_happiness(current_happiness):
                self._optimal_happiness = current_happiness

    @abstractmethod
    def _accept_happiness(self, happiness: int) -> bool:
        pass

    def reset(self):
        self._optimal_happiness = self._starting_happiness


class MaximumHappinessSeatingFinder(SeatingFinder):
    def __init__(self):
        super().__init__(0)

    def _accept_happiness(self, happiness: int) -> bool:
        return happiness >= self._optimal_happiness
