import re
from typing import List, Callable

from monkey import Monkey


class MonkeyFactory:
    @staticmethod
    def hatch(monkey_string: str) -> Monkey:
        monkey_lines = [_.strip(' ') for _ in monkey_string.split('\n')]

        uid = MonkeyFactory.get_uid(monkey_lines[0])
        starting_items = MonkeyFactory.get_starting_items(monkey_lines[1])
        update_func = MonkeyFactory.get_update_func(monkey_lines[2])
        denominator = MonkeyFactory.get_digits(monkey_lines[3])
        true_target = MonkeyFactory.get_digits(monkey_lines[4])
        false_target = MonkeyFactory.get_digits(monkey_lines[5])

        return Monkey(
            uid=uid,
            starting_items=starting_items,
            denominator=denominator,
            true_target=true_target,
            false_target=false_target,
            update_func=update_func
        )

    @staticmethod
    def get_uid(uid_string: str) -> int:
        uid_match = re.match(r'Monkey (\d{1,2}):', uid_string)

        return int(uid_match.group(1))

    @staticmethod
    def get_starting_items(item_string: str) -> List[int]:
        _, items = item_string.split(': ')
        return [int(__) for __ in items.split(', ')]

    @staticmethod
    def get_digits(test_string: str) -> int:
        return int(test_string.split(' ')[-1])

    @staticmethod
    def get_update_func(func_string: str) -> Callable[[int], int]:
        _, operation = func_string.split('= ')

        if '+' in operation:
            return MonkeyFactory.get_addition(operation)

        return MonkeyFactory.get_multiplication(operation)

    @staticmethod
    def get_addition(operation: str) -> Callable[[int], int]:
        _, right = operation.split(' + ')

        if right == 'old':
            def func(item: int) -> int:
                return item + item

        else:
            def func(item: int) -> int:
                return item + int(right)

        return func

    @staticmethod
    def get_multiplication(operation: str) -> Callable[[int], int]:
        _, right = operation.split(' * ')

        if right == 'old':
            def func(item: int) -> int:
                return item * item

        else:
            def func(item: int) -> int:
                return item * int(right)

        return func
