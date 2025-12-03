from initialization import HashMap


def main(filename: str):
    with open(filename, 'r') as _f:
        operations = _f.read().split(',')

    elf_hash_map = HashMap(modulus=256)

    for operation in operations:
        elf_hash_map.perform_operation(operation)

    print(elf_hash_map.focussing_power)


if __name__ == '__main__':
    main('../input.txt')
