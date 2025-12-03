import re


def read_memory_strings(filename: str) -> list[str]:
    with open(filename) as f:
        return [_.strip("\n") for _ in f.readlines()]


def replace_encoded_strings(memory_string: str) -> str:
    new_string = memory_string[:]
    misencoded_strings = re.findall(r"[a-z🎁]\\\\x", memory_string)
    encoded_strings = re.findall(r"\\x[0-9a-f]{2}", memory_string)

    for misencoded_string in misencoded_strings:
        new_string = new_string.replace(misencoded_string, "a\\\\f")

    for encoded_string in encoded_strings:
        new_string = new_string.replace(encoded_string, "🎅")

    return new_string


def replace_escaped_backslashes(memory_string: str) -> str:
    new_string = memory_string.replace("\\\\", "🎄")

    return new_string


def replace_escaped_quotes(memory_string: str) -> str:
    new_string = memory_string.replace("\\\"", "🎁")

    return new_string


def main_one(memory_strings: list[str]) -> int:
    clean_strings = []
    for memory_string in memory_strings:
        clean_strings.append(
            replace_escaped_backslashes(
                replace_encoded_strings(
                    replace_escaped_quotes(
                        memory_string[1:-1]
                    )
                )
            )
        )

    clean_length = sum(len(_) for _ in clean_strings)

    return clean_length


def main_two(memory_strings: list[str]) -> int:
    clean_strings = []

    for memory_string in memory_strings:
        new_string = memory_string.replace("\"", "ab")
        new_string = new_string.replace("\\", "cd")
        clean_strings.append(new_string)

    # +2 for leading and trailing quotes
    clean_length = sum(len(_) + 2 for _ in clean_strings)

    return clean_length


def main(filename: str):
    memory_strings = read_memory_strings(filename)
    full_length = sum(len(_) for _ in memory_strings)
    print(full_length - main_one(memory_strings))
    print(main_two(memory_strings) - full_length)


if __name__ == '__main__':
    main("input.txt")
