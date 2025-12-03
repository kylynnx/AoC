from typing import List, Callable, Tuple


class Monkey:
    def __init__(self, uid: int, starting_items: List[int], denominator: int, true_target: int, false_target: int,
                 update_func: Callable[[int], int]):
        self._id = uid
        self._items = starting_items
        self._denominator = denominator
        self._true_target = true_target
        self._false_target = false_target
        self._update_func = staticmethod(update_func)
        self._inspected_items = 0

    @property
    def id(self):
        return self._id

    @property
    def denominator(self):
        return self._denominator

    @property
    def inspected_items(self):
        return self._inspected_items

    def inspect_items(self, denominator_product: int = None) -> List[Tuple[int, int]]:
        queue = []

        while self._items:
            self._inspected_items += 1
            item = self._items.pop(0)
            new_item = self._update_func(item)

            if denominator_product:
                new_item %= denominator_product
            else:
                new_item //= 3

            if new_item % self._denominator == 0:
                queue.append((self._true_target, new_item))
            else:
                queue.append((self._false_target, new_item))

        return queue

    def get_item(self, item: int):
        self._items.append(item)
