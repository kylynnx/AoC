from file_system_wrapper import FileSystemWrapper


def main(filename: str, limit: int = 100000, file_system_size: int = 70000000, required_size: int = 30000000):
    with open(filename) as _f:
        raw_output = _f.read().strip('$')

    file_system_wrapper = FileSystemWrapper()
    commands = [_.strip('\n').strip(' ') for _ in raw_output.split('$')]

    for command in commands:
        file_system_wrapper.handle_command(command)

    directory_sizes = [_.size for _ in file_system_wrapper.tree]

    print(sum([_ for _ in directory_sizes if _ < limit]))

    size_to_free = required_size - (file_system_size - file_system_wrapper.root.size)
    print(min([_ for _ in directory_sizes if _ >= size_to_free]))


if __name__ == '__main__':
    main('../input.txt')
