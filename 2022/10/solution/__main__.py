from register import Register


def main(filename: str):
    register = Register()

    with open(filename) as _f:
        operations = [_.strip('\n') for _ in _f.readlines()]

    for op in operations:
        register.perform_operation(operation=op)

    print(register.signal_strength)
    print(register.crt)


if __name__ == '__main__':
    main('../input.txt')
