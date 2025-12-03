from monkey_factory import MonkeyFactory
from tree import Tree


def observe_monkeys(filename: str, rounds: int, use_denominator_product: bool = False):
    with open(filename) as _f:
        config = _f.read()

    monkey_configs = [_ for _ in config.split('\n\n')]
    tree = Tree()

    for monkey_config in monkey_configs:
        monkey = MonkeyFactory.hatch(monkey_config)
        tree.add_monkey(monkey)

    tree.observe_rounds(round_count=rounds, use_denominator_product=use_denominator_product)
    print(tree.monkey_business)


def main(filename: str):
    observe_monkeys(filename, 20)
    observe_monkeys(filename, 10000, True)


if __name__ == '__main__':
    main('../input.txt')
