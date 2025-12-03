import re
from copy import copy

from directory_wrapper import DirectoryWrapper


class FileSystemWrapper:
    def __init__(self):
        self._current_path = []
        self._root_directory = DirectoryWrapper()
        self._dir_list = []

    def add_directory(self, name: str):
        self._root_directory.add_directory(copy(self._current_path), name)

    def add_file(self, size: int):
        self._root_directory.add_file(copy(self._current_path), size)

    def handle_command(self, command: str):
        if command.startswith('cd'):
            self._handle_cd(command)
        else:
            self._handle_ls(command)

    def _handle_cd(self, command: str):
        command_match = re.match(r'^cd (.+)$', command)
        match command_match.group(1):
            case '/':
                self._current_path = []
            case '..':
                self._current_path.pop(-1)
            case _:
                self._current_path.append(command_match.group(1))

    def _handle_ls(self, command: str):
        command_output = command.split('\n')[1:]

        for output_line in command_output:
            dir_match = re.match(r'dir ([a-z]+)', output_line)
            if dir_match:
                self.add_directory(dir_match.group(1))
            else:
                size_match = re.match(r'([0-9]+) [a-z.]+', output_line)
                self.add_file(int(size_match.group(1)))

    @property
    def tree(self):
        return self._root_directory.tree

    @property
    def dir_count(self):
        return 1 + self._root_directory.dir_count

    @property
    def root(self):
        return self._root_directory
