import re

from block import Block
from block_base import BlockBase


class BlockFactory:
    @staticmethod
    def produce(block_string: str) -> Block:
        match = re.match(r'(\d{1,4}),(\d{1,4}),(\d{1,4})~(\d{1,4}),(\d{1,4}),(\d{1,4})', block_string)

        start_x = int(match.group(1))
        start_y = int(match.group(2))
        height = int(match.group(3))

        end_x = int(match.group(4))
        end_y = int(match.group(5))
        length = int(match.group(6)) - height + 1

        return Block(
            base=BlockBase(
                start_x=start_x, end_x=end_x,
                start_y=start_y, end_y=end_y
            ),
            height=height,
            length=length
        )
