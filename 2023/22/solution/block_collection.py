from typing import Set

from block_factory import BlockFactory


class BlockCollection:
    def __init__(self, filename: str):
        with open(filename, 'r') as _f:
            blocks = [BlockFactory.produce(_.strip('\n')) for _ in _f.readlines()]
        blocks.sort()

        self._blocks = blocks
        self._height_map = {}
        self._let_gravity_act()
        self._removable_blocks = None
        self._supports_map = {}
        self._supported_by_map = {}
        self._falling_blocks = None

    def _let_gravity_act(self):
        _new_blocks = []

        for block in self._blocks:
            _new_z = block.height + 1

            blocked_below = False
            while not blocked_below:
                _new_z -= 1

                if _new_z == 0:
                    blocked_below = True

                if _new_z - 1 in self._height_map:
                    lower_blocks = self._height_map[_new_z - 1]

                    if any(block.base.overlap(_new_blocks[_].base) for _ in lower_blocks):
                        blocked_below = True

            block.height = _new_z
            if (map_key := _new_z + block.length - 1) in self._height_map:
                self._height_map[map_key].append(len(_new_blocks))
            else:
                self._height_map[map_key] = [len(_new_blocks)]

            _new_blocks.append(block)

        self._blocks = _new_blocks

    def _set_support_maps(self):
        max_z = max(self._height_map.keys())
        min_z = min(self._height_map.keys())
        check_z = max_z

        while check_z > min_z:
            if check_z in self._height_map:
                block_indices = self._height_map[check_z]

                for block_index in block_indices:
                    check_block = self._blocks[block_index]
                    support_block_indices = set()

                    if (check_height := check_block.height - 1) < 0:
                        continue

                    for support_block_index in self._height_map[check_height]:
                        if check_block.base.overlap(self._blocks[support_block_index].base):
                            support_block_indices.add(support_block_index)

                            if support_block_index in self._supports_map:
                                self._supports_map[support_block_index].add(block_index)
                            else:
                                self._supports_map[support_block_index] = {block_index}

                    self._supported_by_map[block_index] = support_block_indices

            check_z -= 1

    @property
    def removable_blocks(self):
        if self._removable_blocks is None:
            if not self._supports_map:
                self._set_support_maps()

            cannot_be_removed = set(
                list(supported_by)[0] for supported_by in self._supported_by_map.values() if len(supported_by) == 1
            )

            self._removable_blocks = len(self._blocks) - len(cannot_be_removed)

        return self._removable_blocks

    @property
    def falling_blocks(self):
        if self._falling_blocks is None:
            if not self._supported_by_map:
                self._set_support_maps()

            max_index = max(self._supported_by_map.keys())
            current_index = max_index
            falling_sum = 0

            def count_falling_blocks(block_index: int, falling_indices: Set[int] = None) -> Set[int]:
                if falling_indices is None:
                    falling_indices = set()
                    is_first_block = True
                else:
                    falling_indices = set(falling_indices)
                    is_first_block = False

                if block_index not in self._supports_map or len(self._supports_map[block_index]) == 0:
                    return falling_indices

                if (
                        block_index not in self._supported_by_map
                        or set(self._supported_by_map[block_index]).issubset(falling_indices)
                        or not falling_indices
                ):
                    falling_indices.add(block_index)
                    if block_index in self._supports_map:
                        supported = {
                            _ for _ in self._supports_map[block_index]
                            if self._supported_by_map[_].issubset(falling_indices)
                        }
                        falling_indices = falling_indices.union(supported)
                        for supported_block_index in supported:
                            falling_indices = falling_indices.union(
                                count_falling_blocks(supported_block_index, falling_indices)
                            )
                    if is_first_block:
                        falling_indices.remove(block_index)

                    return falling_indices

                return falling_indices

            while current_index >= 0:
                falling_sum += len(count_falling_blocks(current_index))
                current_index -= 1

            self._falling_blocks = falling_sum

        return self._falling_blocks
