class IDRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, item: int) -> bool:
        return self.start <= item <= self.end

    def __repr__(self):
        return f"({self.start}, {self.end})"

    def ids(self):
        return list(range(self.start, self.end + 1))


class InvalidIDRange:
    def __init__(self, length: int, repetitions: int = 2):
        self.factor = sum(10 ** (_ * length) for _ in range(repetitions))
        self.start = 10 ** (length - 1) * self.factor
        self.end = (10 ** length - 1) * self.factor

    def __repr__(self):
        return f"{self.factor}, ({self.start}, {self.end})"

    def __contains__(self, item: int) -> bool:
        return item % self.factor == 0 and self.start <= item <= self.end


def main(filename: str):
    with open(filename, "r") as f:
        id_ranges = [
            IDRange(*[int(value) for value in id_range.split("-")]) for id_range in f.read().split(',')
        ]

    invalid_id_sum = calculate_invalid_id_sum(id_ranges)
    print(f"The sum of the invalid IDs is {invalid_id_sum}.")

    invalid_id_sum_new_rules = calculate_invalid_id_sum(id_ranges=id_ranges, max_repetitions=None)
    print(f"With the new rules the sum of all invalid IDs is {invalid_id_sum_new_rules}.")


def calculate_invalid_id_sum(id_ranges: list[IDRange], min_repetitions: int = 2,
                               max_repetitions: int | None = 2) -> int:
    invalid_id_sum = 0

    for id_range in id_ranges:
        upper_bound = max_repetitions if max_repetitions is not None else len(str(id_range.end))

        invalid_id_ranges = []
        for repetitions in range(min_repetitions, upper_bound + 1):
            min_length = max(1, len(str(id_range.start)) // repetitions)
            max_length = len(str(id_range.end)) // repetitions

            for length in range(min_length, max_length + 1):
                invalid_id_ranges.append(InvalidIDRange(length=length, repetitions=repetitions))

        invalid_id_sum += sum(
            set(idx for idx in id_range.ids()
            if any(idx in invalid_range for invalid_range in invalid_id_ranges))
        )

    return invalid_id_sum


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
