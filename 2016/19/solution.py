from collections import deque


def main(elf_count: int):
    elfs = [_ + 1 for _ in range(elf_count)]

    while len(elfs) > 1:
        elfs = move_presents(elfs)

    elf_with_presents = elfs[0]

    print(f"Elf {elf_with_presents} has all presents at the end.")

    elf_with_presents = find_elf_opposite_stealing(elf_count)
    print(f"When stealing opposite, Elf {elf_with_presents} has all presents at the end.")


def move_presents(elfs: list[int]) -> list[int]:
    new_elfs = []

    if len(elfs) % 2 == 1:
        new_elfs.append(elfs[-1])

    new_elfs += elfs[:-1:2]

    return new_elfs


def josephus(elfs: int) -> int:
    # Found this after having implemented the above
    # https://en.wikipedia.org/wiki/Josephus_problem
    return int(bin(elfs)[3:] + bin(elfs)[2], 2)


def find_elf_opposite_stealing(elf_count: int) -> int:
    left = deque([_ + 1 for _ in range(elf_count // 2)])
    right = deque([_ + elf_count // 2 + 1 for _ in range(elf_count // 2)])

    while left and right:
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()

        right.appendleft(left.popleft())
        left.append(right.pop())

    return left[0] or right[0]


if __name__ == "__main__":
    main(elf_count=5)
    print("")
    main(elf_count=3005290)
