from assignment_range import AssignmentRange


class AssignmentSet:
    def __init__(self, assignment_string: str):
        ranges = assignment_string.split(',')
        self._left = AssignmentRange(*[int(_) for _ in ranges[0].split('-')])
        self._right = AssignmentRange(*[int(_) for _ in ranges[1].split('-')])

    @property
    def redundant(self) -> bool:
        return self._left in self._right or self._right in self._left

    def overlaps(self):
        return self._left.overlaps(self._right)
