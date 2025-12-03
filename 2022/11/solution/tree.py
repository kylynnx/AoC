import math
from typing import Dict

from monkey import Monkey


class Tree:
    def __init__(self):
        self._monkeys: Dict[int, Monkey] = {}
        self._queue = []
        self._rounds = 0
        self._denominator_product = None

    def add_monkey(self, monkey: Monkey):
        self._monkeys[monkey.id] = monkey
        self._queue.append(monkey.id)

    def observe_rounds(self, round_count: int = 20, use_denominator_product: bool = False):
        self._queue.append(None)
        if use_denominator_product:
            self._denominator_product = math.prod(_.denominator for _ in self._monkeys.values())

        while self._rounds < round_count:
            current_monkey = self._queue.pop(0)
            self._queue.append(current_monkey)
            if current_monkey is None:
                self._rounds += 1
                continue

            thrown_targeted_items = self._monkeys[current_monkey].inspect_items(
                denominator_product=self._denominator_product
            )

            for target, item in thrown_targeted_items:
                self._monkeys[target].get_item(item)

    @property
    def monkey_business(self):
        inspections = [_.inspected_items for _ in self._monkeys.values()]
        inspections.sort(reverse=True)

        return math.prod(inspections[:2])
