import string


class PasswordGenerator:
    _letters = string.ascii_lowercase
    _range = len(string.ascii_lowercase)

    @classmethod
    def generate(cls, current: str) -> str:
        current_index = len(current) - 1
        increase_next = True
        new_password = ""

        while current_index >= 0 and increase_next:
            new_letter, increase_next = cls.increase_letter(current[-1])
            new_password = f"{new_letter}{new_password}"
            current = current[:-1]
            current_index -= 1

        new_password = f"{current}{new_password}"

        return new_password

    @classmethod
    def increase_letter(cls, letter: str) -> (str, bool):
        current_index = cls._letters.index(letter)
        new_index = (current_index + 1) % cls._range

        return cls._letters[new_index], new_index < current_index
