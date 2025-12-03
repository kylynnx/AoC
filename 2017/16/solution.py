import string


def main(filename: str):
    with open(filename, "r") as f:
        commands = [_ for _ in f.read().strip().split(",")]

    line = [_ for _ in string.ascii_lowercase[:16]]
    steps = 0
    permutation_map = {}
    seen_permutations = set()

    while (line_str := "".join(line)) not in seen_permutations and steps < 1e9:
        seen_permutations.add("".join(line))
        permutation_map[steps] = line_str
        for command in commands:
            line = execute_command(command=command, line=line)
        steps += 1

    print(f"After their dance the programs are in this order: `{permutation_map[1]}`")
    print(f"The order after one billion dances is {permutation_map[1e9 % steps]}.")


def execute_command(command: str, line: list) -> list:
    command_id, args = command[:1], command[1:]

    match command_id:
        case "s":
            return spin(line=line, steps=int(args))
        case "x":
            one, two = args.split("/")
            return exchange(line=line, positions=(int(one), int(two)))
        case "p":
            name_one, name_two = args.split("/")
            return partner(line=line, names=(name_one, name_two))
        case _:
            raise ValueError("Unknown command")


def spin(line: list[str], steps: int) -> list[str]:
    return line[-steps:] + line[:-steps]


def exchange(line: list[str], positions: tuple[int, int]) -> list[str]:
    one, two = positions
    line[one], line[two] = line[two], line[one]

    return line


def partner(line: list[str], names: tuple[str, str]) -> list[str]:
    name_one, name_two = names
    positions = (line.index(name_one), line.index(name_two))

    return exchange(line=line, positions=positions)


if __name__ == "__main__":
    assert spin(["a", "b", "c", "d", "e"], 1) == ["e", "a", "b", "c", "d"]
    assert exchange(["e", "a", "b", "c", "d"], (3, 4)) == ["e", "a", "b", "d", "c"]
    assert partner(["e", "a", "b", "d", "c"], ("e", "b")) == ["b", "a", "e", "d", "c"]

    main("input.txt")
