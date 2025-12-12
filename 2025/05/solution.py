from typing import NamedTuple


class Range(NamedTuple):
    min: int
    max: int

    @property
    def element_count(self) -> int:
        return self.max - self.min + 1

    def __lt__(self, other: Range) -> bool:
        return self.min < other.min or (self.min == other.min and self.max < other.max)

    def overlaps(self, other: Range) -> bool:
        return (
            (
                self.min <= other.min <= self.max
            )
            or
            (
                other.min <= self.min <= other.max
            )
        )

    def join(self, other: Range) -> Range:
        return Range(min(self.min, other.min), max(self.max, other.max))


def main(filename: str):
    with open(filename) as f:
        ranges, available_ids = f.read().split("\n\n")

    available_ids = [int(_) for _ in available_ids.split("\n")]
    ranges = [Range(*(int(v) for v in _.split("-"))) for _ in ranges.split("\n")]

    fresh_ids = [_ for _ in available_ids if any(r.min <= _ <= r.max for r in ranges)]
    print(f"Of the available IDs {len(fresh_ids)} are fresh.")

    ranges.sort()
    joined_ranges = []
    current_range = ranges.pop(0)

    while ranges:
        next_range = ranges.pop(0)

        if current_range.overlaps(next_range):
            current_range = current_range.join(next_range)
        else:
            joined_ranges.append(current_range)
            current_range = next_range

    joined_ranges.append(current_range)

    fresh_id_count = sum(_.element_count for _ in joined_ranges)
    print(f"In total {fresh_id_count} ingredient IDs are considered fresh.")


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
