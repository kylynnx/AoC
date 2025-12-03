from itertools import product


class Matrix:
    def __init__(self, idx: str):
        self.idx = idx
        self.rows = [[_ for _ in row] for row in idx.split("/")]
        self.dimension = len(self.rows)
        self.pixel_count = sum(sum(_ == "#" for _ in row) for row in self.rows)

    def rotate(self) -> "Matrix":
        # Transpose
        transposed_rows = [[""] * self.dimension for _ in range(self.dimension)]
        for column in range(self.dimension):
            for row in range(self.dimension):
                transposed_rows[column][row] = self.rows[row][column]

        # Flip columns
        new_idx = ""
        for row in range(self.dimension):
            new_idx += "".join(transposed_rows[self.dimension - row - 1]) + "/"

        return Matrix(new_idx[:-1])

    def flip_vertical(self) -> "Matrix":
        return Matrix("/".join(["".join(_)[::-1] for _ in self.rows]))

    def flip_horizontal(self) -> "Matrix":
        return Matrix("/".join("".join(_) for _ in reversed(self.rows)))

    def split_into_parts(self, divisor: int) -> list[str]:
        new_dimension = self.dimension // divisor
        idxs = []

        for row_offset in range(divisor):
            idxs_from_from_row = []
            for row_count in range(new_dimension):
                source_row = (row_offset * new_dimension) + row_count
                new_rows = [
                    "".join(self.rows[source_row][_ * new_dimension: _ * new_dimension + new_dimension])
                    for _ in range(divisor)
                ]

                if not idxs_from_from_row:
                    idxs_from_from_row = new_rows
                else:
                    for n_part in range(len(new_rows)):
                        idxs_from_from_row[n_part] += "/" + new_rows[n_part]
            idxs += idxs_from_from_row

        return idxs

    @classmethod
    def from_parts(cls, parts: list["Matrix"], parts_per_row: int) -> "Matrix":
        split_part_idxs = [_.idx.split("/") for _ in parts]
        part_dimension = len(split_part_idxs[0][0])

        rows = []

        for n_rows in range(parts_per_row):
            for n_combine in range(part_dimension):
                rows.append(
                    "".join(split_part_idxs[(n_rows * parts_per_row) + _][n_combine] for _ in range(parts_per_row))
                )

        return Matrix("/".join(rows))


def find_rule(matrix: Matrix, rules: dict[str, str]) -> tuple[str | None, list[str]]:
    rotations = 0
    add_to_rules = []

    while matrix.idx not in rules and rotations < 3:
        rotations += 1
        add_to_rules.append(matrix.idx)
        matrix = matrix.rotate()

    if matrix.idx in rules:
        new_idx = rules[matrix.idx]

        for idx in add_to_rules:
            rules[idx] = new_idx

        return new_idx, []

    return None, add_to_rules


def evolve_matrix(matrix: Matrix, rules: dict[str, str]) -> Matrix | None:
    flipped_vertically = matrix.flip_vertical()
    flipped_horizontally = matrix.flip_horizontal()

    new_idx, add_to_rule = find_rule(matrix, rules=rules)
    if new_idx is None:
        new_idx, new_add = find_rule(flipped_vertically, rules=rules)
        add_to_rule += new_add
    if new_idx is None:
        new_idx, new_add = find_rule(flipped_horizontally, rules=rules)
        add_to_rule += new_add

    for idx in add_to_rule:
        rules[idx] = new_idx

    return Matrix(new_idx)


def build_evolutions(rules: dict[str, str]) -> dict[str, tuple[int, int, int, list[str]]]:
    partials = ["...", "..#", ".#.", ".##", "#..", "#.#", "##.", "###"]
    matrix_idxs = set("/".join(_) for _ in product(partials, repeat=3))

    evolutions = dict()

    for matrix_idx in matrix_idxs:
        matrix = Matrix(matrix_idx)
        initial_count = matrix.pixel_count

        four = evolve_matrix(matrix=matrix, rules=rules)

        threes_from_four = [evolve_matrix(Matrix(_), rules=rules) for _ in four.split_into_parts(divisor=2)]

        six = Matrix.from_parts(parts=threes_from_four, parts_per_row=2)

        threes_from_six = [evolve_matrix(Matrix(_), rules=rules) for _ in six.split_into_parts(divisor=3)]
        nine_ids = [_.idx for _ in threes_from_six]

        evolutions[matrix_idx] = (initial_count, four.pixel_count, six.pixel_count, nine_ids)

    return evolutions


def main(filename: str, initial_state: str, iterations: int):
    with open(filename) as f:
        rule_strings = [_.strip() for _ in f.readlines()]

    rules = {}

    for rule_string in rule_strings:
        src, tgt = rule_string.split(" => ")
        rules[src] = tgt

    evolutions = build_evolutions(rules=rules)

    queue = [initial_state]
    iteration = 0
    max_evolution_iterations = iterations // 3

    while iteration < max_evolution_iterations:
        new_queue = []
        for matrix in queue:
            new_queue += evolutions[matrix][3]
        iteration += 1
        queue = new_queue

    remainder = iterations - iteration * 3
    lit_pixels = sum(evolutions[_][remainder] for _ in queue)
    print(f"After {iterations} iterations {lit_pixels} pixels stay on.")


if __name__ == "__main__":
    main("input.txt", initial_state=".#./..#/###", iterations=5)
    main("input.txt", initial_state=".#./..#/###", iterations=18)

