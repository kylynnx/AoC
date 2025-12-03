def main(filename: str):
    with open(filename) as f:
        lines = [_.strip("\n") for _ in f.readlines()]

    valid_passphrases = 0
    valid_anagram_passphrases = 0

    for line in lines:
        word_list = line.split(" ")
        word_set = set(word_list)

        if len(word_set) == len(word_list):
            valid_passphrases += 1

        sorted_word_list = ["".join(sorted(_)) for _ in word_list]
        sorted_word_set = set(sorted_word_list)

        if len(sorted_word_set) == len(sorted_word_list):
            valid_anagram_passphrases += 1

    print(f"The file contains {valid_passphrases} valid passphrases.")
    print(f"The file contains {valid_anagram_passphrases} valid passphrases without anagrams.")


if __name__ == "__main__":
    main("input.txt")
