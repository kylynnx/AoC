from assignment_set import AssignmentSet


def main(filename: str):
    with open(filename, 'r') as _f:
        assignment_lines = [_.strip('\n') for _ in _f.readlines()]

    assignment_sets = [AssignmentSet(_) for _ in assignment_lines]

    print(sum(_.redundant for _ in assignment_sets))

    print(sum(_.overlaps() for _ in assignment_sets))


if __name__ == '__main__':
    main('../input.txt')
