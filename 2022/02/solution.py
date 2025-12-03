first_guide = {
    'A X': 4,
    'A Y': 8,
    'A Z': 3,

    'B X': 1,
    'B Y': 5,
    'B Z': 9,

    'C X': 7,
    'C Y': 2,
    'C Z': 6
}

second_guide = {
    'A X': 3,
    'A Y': 4,
    'A Z': 8,

    'B X': 1,
    'B Y': 5,
    'B Z': 9,

    'C X': 2,
    'C Y': 6,
    'C Z': 7
}


def first_strategy(filename: str):
    with open(filename, 'r') as _f:
        scores = [first_guide[_.strip('\n')] for _ in _f.readlines()]

    print(sum(scores))


def second_strategy(filename: str):
    with open(filename, 'r') as _f:
        scores = [second_guide[_.strip('\n')] for _ in _f.readlines()]

    print(sum(scores))


def main(filename: str):
    first_strategy(filename)
    second_strategy(filename)


if __name__ == '__main__':
    main('input.txt')
