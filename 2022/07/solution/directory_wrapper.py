from typing import List


class DirectoryWrapper:
    def __init__(self):
        self._size = 0
        self._subdirectories = {}

    def add_file(self, path: List[str], size: int):
        if len(path):
            sub_directory = path.pop(0)

            if sub_directory not in self._subdirectories:
                raise ValueError(f"Subdirectory {sub_directory} does not exist")

            return self._subdirectories[sub_directory].add_file(path, size)
        self._size += size

    def add_directory(self, path: List[str], directory: str):
        if len(path):
            sub_directory = path.pop(0)

            if sub_directory not in self._subdirectories:
                raise ValueError(f"Subdirectory {sub_directory} does not exist")

            return self._subdirectories[sub_directory].add_directory(path, directory)

        self._subdirectories[directory] = DirectoryWrapper()

    @property
    def size(self):
        subdirectories_size = sum(_.size for _ in self._subdirectories.values())
        return subdirectories_size + self._size

    @property
    def tree(self):
        _tree = [self]

        for sudbir in self._subdirectories.values():
            _tree += sudbir.tree

        return _tree

    @property
    def dir_count(self):
        return 1 + sum([_.dir_count for _ in self._subdirectories.values()])
