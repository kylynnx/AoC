from enum import Enum
from math import prod


class Operator(Enum):
    ADD = "+"
    MULTIPLY = "*"


def main(filename: str):
    with open(filename) as f:
        *raw_lines, operators = [_.replace("\n", "") for _ in f.readlines()]

    lines = [[int(_) for _ in line.split()] for line in raw_lines]
    operands = [tuple(line[exercise] for line in lines) for exercise in range(len(lines[0]))]
    operators = [Operator(_) for _ in operators.split()]

    grand_total = solve_problems(operators=operators, operands=operands)
    print(f"Reading horizontally the grand total is {grand_total}.")

    vertical_operands = load_problems_vertically(raw_lines)
    vertical_grand_total = solve_problems(operators=operators, operands=vertical_operands)
    print(f"Vertically the grand total is {vertical_grand_total}.")


def load_problems_vertically(lines: list[str]) -> list[tuple[int, ...]]:
    operands = []
    while all(" " in _ for _ in lines):
        split_at = max(_.index(" ") for _ in lines)
        parts = [_[:split_at] for _ in lines]
        lines = [_[split_at + 1:] for _ in lines]

        operands.append(
            tuple(
                int("".join(_[position] for _ in parts))
                for position in range(split_at)
            )
        )

    last_length = len(max(lines, key=len))
    lines = [_ + " " * (last_length - len(_)) for _ in lines]
    operands.append(
        tuple(
            int("".join(_[position] for _ in lines))
            for position in range(last_length)
        )
    )

    return operands


def solve_problems(operators: list[Operator], operands: list[tuple[int, ...]]) -> int:
    grand_total = 0

    for operator, values in zip(operators, operands):
        if operator == Operator.ADD:
            grand_total += sum(values)
        else:
            grand_total += prod(values)

    return grand_total


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
