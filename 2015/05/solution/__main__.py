from word_checker import WordChecker
from rules import (
    ThreeVowelRule, DoubleLetterRule, NaughtyStringRule, RepeatingDoubleLetterRule, RepeatingSingleLetterRule
)


def main(filename: str):
    with open(filename) as f:
        words = f.readlines()

    word_checker_one = WordChecker([ThreeVowelRule, DoubleLetterRule, NaughtyStringRule])
    nice_words_one = word_checker_one.check(words)
    print(nice_words_one)

    word_checker_two = WordChecker([RepeatingSingleLetterRule, RepeatingDoubleLetterRule])
    nice_words_two = word_checker_two.check(words)
    print(nice_words_two)


if __name__ == '__main__':
    main("../input.txt")
