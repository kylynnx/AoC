from password_checker import PasswordChecker
from password_generator import PasswordGenerator
from rules import ForbiddenLetterRule, IncreasingLetterStraightRule, LetterPairRule


def main(password: str):
    password_checker = PasswordChecker([ForbiddenLetterRule, LetterPairRule, IncreasingLetterStraightRule])
    while not password_checker.check(password):
        password = PasswordGenerator.generate(password)

    print(password)

    password = PasswordGenerator.generate(password)
    while not password_checker.check(password):
        password = PasswordGenerator.generate(password)
    print(password)


if __name__ == '__main__':
    main("hxbxwxba")
