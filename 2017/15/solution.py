class NumberGenerator:
    def __init__(self, factor: int, modulus: int, start: int):
        self.factor = factor
        self.modulus = modulus
        self.prev = start

    def __iter__(self):
        return self

    def __next__(self):
        return self._next()

    def _next(self):
        next_number = (self.prev * self.factor) % self.modulus
        self.prev = next_number
        return next_number


class MultipleNumberGenerator(NumberGenerator):
    def __init__(self, base: int, factor: int, modulus: int, start: int):
        super().__init__(factor=factor, modulus=modulus, start=start)
        self.base = base

    def _next(self):
        next_number = super()._next()
        while not next_number % self.base == 0:
            next_number = super()._next()

        return next_number


def main(filename: str):
    with open(filename) as file:
        start_a, start_b = [int(_.strip().split(" ")[-1]) for _ in file.readlines()]

    gen_a = NumberGenerator(start=start_a, factor=16807, modulus=2147483647)
    gen_b = NumberGenerator(start=start_b, factor=48271, modulus=2147483647)
    matches = 0

    for _ in range(int(40e6)):
        num_a = next(gen_a)
        num_b = next(gen_b)

        if bin(num_a)[-16:] == bin(num_b)[-16:]:
            matches += 1

    print(f"The generators produce {matches} matching numbers.")

    mul_gen_a = MultipleNumberGenerator(start=start_a, factor=16807, modulus=2147483647, base=4)
    mul_gen_b = MultipleNumberGenerator(start=start_b, factor=48271, modulus=2147483647, base=8)
    matches = 0

    for _ in range(int(5e6)):
        num_a = next(mul_gen_a)
        num_b = next(mul_gen_b)

        if bin(num_a)[-16:] == bin(num_b)[-16:]:
            matches += 1

    print(f"With the divisibility conditions the judge's final count is {matches}.")


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
