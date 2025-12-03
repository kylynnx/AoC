from block_base import BlockBase


class Block:
    def __init__(self, base: BlockBase, height: int, length: int):
        self._base = base
        self._height = height
        self._length = length

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value

    @property
    def length(self):
        return self._length

    @property
    def base(self):
        return self._base

    def __lt__(self, other: 'Block'):
        return self._height < other.height
