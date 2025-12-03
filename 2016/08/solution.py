import re
import string

from pyfiglet import Figlet


class Display:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._grid = [False] * self._width * self._height

    def __str__(self):
        display_string = ""

        for position in range(len(self._grid)):
            display_string += "#" if self._grid[position] else " "
            if (position + 1) % self._width == 0:
                display_string += "\n"

        return display_string

    def read_display_segment(self, width: int, start: int):
        segment_string = ""
        for n_row in range(self._height):
            row_offset = n_row * self._width
            line_start = start + row_offset
            line_end = line_start + width
            segment_string += "".join(["#" if _ else " " for _ in self._grid[line_start:line_end]]) + "\n"
        return segment_string


    @property
    def lit_pixels(self):
        return sum(self._grid)

    @property
    def width(self):
        return self._width

    def execute_command(self, command: str):
        if "rect" in command:
            self._execute_rect(command)
        elif "row" in command:
            self._execute_row_rotation(command)
        else:
            self._execute_column_rotation(command)

    def _execute_rect(self, command: str):
        match = re.search(r"rect (\d+)x(\d+)", command)
        width = int(match.group(1))
        height = int(match.group(2))

        for n_horizontal in range(width):
            for n_vertical in range(height):
                self._grid[n_horizontal + n_vertical * self._width] = True

    def _read_row(self, y: int):
        return self._grid[y * self._width:(y + 1) * self._width]

    def _write_row(self, y: int, content: list[bool]):
        self._grid[y * self._width:(y + 1) * self._width] = content

    def _execute_row_rotation(self, command: str):
        match = re.search(r"rotate row y=(\d+) by (\d+)", command)
        target_row = int(match.group(1))
        rotation = int(match.group(2))
        entries = self._read_row(target_row)
        entries = entries[-rotation:] + entries[:-rotation]
        self._write_row(y=target_row, content=entries)

    def _read_column(self, x: int):
        return self._grid[x::self._width]

    def _write_column(self, x: int, content: list[bool]):
        self._grid[x::self._width] = content

    def _execute_column_rotation(self, command: str):
        match = re.search(r"rotate column x=(\d+) by (\d+)", command)
        target_column = int(match.group(1))
        rotation = int(match.group(2))
        entries = self._read_column(target_column)
        entries = entries[-rotation:] + entries[:-rotation]
        self._write_column(x=target_column, content=entries)


def create_character_lookup():
    # more fonts here: http://www.figlet.org/examples.html
    figlet = Figlet(font="5x7")
    char_lookup = {}
    for character in string.ascii_uppercase:
        rendered_character = str(figlet.renderText(character)).strip("\n").rstrip(" ")
        trimmed_character = "\n".join(_[:-1] for _ in rendered_character.split("\n"))
        char_lookup[trimmed_character] = character
        char_lookup[character] = trimmed_character

    # special cases:
    letter_y = Figlet(font="5x8").renderText("Y")
    letter_y = "\n".join(_[:-1] for _ in letter_y.split("\n")[2:-2]) + "\n"
    char_lookup[letter_y] = "Y"
    char_lookup["Y"] = letter_y

    return char_lookup


def read_display(display: Display, letter_width: int = 5, character_lookup: dict | None = None) -> str:
    letter_count = display.width // letter_width
    result = ""

    if character_lookup is None:
        character_lookup = create_character_lookup()

    for n_letter in range(letter_count):
        letter = display.read_display_segment(width=letter_width, start=n_letter * letter_width)
        if letter in character_lookup:
            character = character_lookup[letter]
            result += character
        else:
            print("Could not find letter")
            print(letter)
            print(character_lookup[solution[n_letter]])
            break
    return result


def main(width: int, height: int, command_file: str, read: bool = True):
    with open(command_file) as f:
        commands = [_.strip("\n") for _ in f.readlines()]

    display = Display(width=width, height=height)

    for command in commands:
        display.execute_command(command)

    print(display)
    print(f"This display has {display.lit_pixels} lit pixels.")
    if read:
        display_text = read_display(display, letter_width=5)
        print(f"This display reads '{display_text}'.")



if __name__ == '__main__':
    main(width=7, height=3, command_file="test.txt", read=False)
    print("\n\n")
    main(width=50, height=6, command_file="input.txt")
