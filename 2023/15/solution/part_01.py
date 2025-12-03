from elf_hash import elf_hash_function


def main(filename: str):
    with open(filename, 'r') as _f:
        initialization = _f.read().split(',')

    _result = 0
    for step in initialization:
        _result += elf_hash_function(initialization_step=step, modulus=256)

    print(_result)


if __name__ == '__main__':
    main(filename='../input.txt')
