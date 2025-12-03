from crate_system import CrateSystem


def main_part_one(filename: str):
    with open(filename, 'r') as _f:
        config = _f.read()

    crate_config, operations = config.split('\n\n')
    crate_system = CrateSystem(crate_config)

    for operation in operations.split('\n'):
        crate_system.perform_operation_9000(operation)

    print(crate_system.top_crates)


def main_part_two(filename: str):
    with open(filename, 'r') as _f:
        config = _f.read()

    crate_config, operations = config.split('\n\n')
    crate_system = CrateSystem(crate_config)

    for operation in operations.split('\n'):
        crate_system.perform_operation_9001(operation)

    print(crate_system.top_crates)


def main(filename: str):
    main_part_one(filename)
    main_part_two(filename)


if __name__ == '__main__':
    main('../input.txt')
