def main(filename: str):
    with open(filename) as f:
        banks = [load_bank(_.strip()) for _ in f.readlines()]

    optimal_joltage = sum(get_optimal_joltage(_) for _ in banks)
    print(f"The optimal joltage is {optimal_joltage}.")

    enahnced_optimal_joltage = sum(get_optimal_joltage(_, digits=12) for _ in banks)
    print(f"With 12 batteries per bank the optimal joltage is {enahnced_optimal_joltage}.")


def load_bank(labels: str) -> list[int]:
    return [int(_) for _ in labels]


def get_optimal_joltage(bank: list[int], digits: int = 2) -> int:
    joltage_digits = []
    start = 0
    for digit in range(1, digits + 1):
        end = len(bank) - (digits - digit)
        max_digit = max(bank[start: end])
        joltage_digits.append(max_digit)
        start += bank[start:end].index(max_digit) + 1

    return int("".join(str(_) for _ in joltage_digits))


if __name__ == "__main__":
    test_cases = [
        ("987654321111111", [(2, 98), (12, 987654321111)]),
        ("811111111111119", [(2, 89), (12, 811111111119)]),
        ("234234234234278", [(2, 78), (12, 434234234278)]),
        ("818181911112111", [(2, 92), (12, 888911112111)]),
    ]

    for test_labels, test_configurations in test_cases:
        test_bank = load_bank(test_labels)
        for test_digits, expected_joltage in test_configurations:
            assert get_optimal_joltage(bank=test_bank, digits=test_digits) == expected_joltage


    main("input.txt")
