def find_marker(comm_string: str, marker_length: int) -> int:
    current_start = 0
    while current_start < len(comm_string) - marker_length:
        received_letters = comm_string[current_start:current_start + marker_length]
        if len(received_letters) == len(set(received_letters)):
            return current_start + marker_length

        current_start += 1


def main(filename: str):
    with open(filename) as _f:
        communications = [_.strip('\n') for _ in _f.readlines()]

    for communication in communications:
        print(find_marker(communication, marker_length=4))
        print(find_marker(communication, marker_length=14))


if __name__ == '__main__':
    main('input.txt')
