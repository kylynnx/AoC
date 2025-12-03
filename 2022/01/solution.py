def main(filename: str):
    with open(filename, 'r') as _f:
        elves_config = _f.read()

    elves = []
    for elf_config in elves_config.split('\n\n'):
        elves.append(sum([int(_) for _ in elf_config.split('\n')]))

    print(max(elves))

    elves.sort(reverse=True)

    print(sum(elves[:3]))


if __name__ == '__main__':
    main('./input.txt')
