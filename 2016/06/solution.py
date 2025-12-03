from collections import defaultdict


def main(filename: str):
    with open(filename) as f:
        lines = [_.strip() for _ in f.readlines()]

    letter_map = defaultdict(list)
    for line in lines:
        for index, letter in enumerate(line):
            letter_map[index].append(letter)

    max_message = [None] * (max(letter_map.keys()) + 1)
    min_message = [None] * (max(letter_map.keys()) + 1)

    for position, letters in letter_map.items():
        unique_letters = set(letters)
        letter_string = "".join(letters)
        letter_counts = {letter: letter_string.count(letter) for letter in unique_letters}

        max_letter = max(letter_counts, key=letter_counts.get)
        max_message[position] = max_letter

        min_letter = min(letter_counts, key=letter_counts.get)
        min_message[position] = min_letter

    print(f"Part 1: {"".join(max_message)}")
    print(f"Part 2: {"".join(min_message)}")


if __name__ == '__main__':
    main("input.txt")
