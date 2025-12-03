from block_collection import BlockCollection


def main(filename: str):
    block_collection = BlockCollection(filename)
    print(block_collection.removable_blocks)
    print(block_collection.falling_blocks)


if __name__ == '__main__':
    main('../input.txt')
