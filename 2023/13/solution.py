from typing import List


class Note:
    def __init__(self, notes_string: str):
        self._notes = notes_string.split('\n')
        self._transposed = None
        self._horizontal_mirror_score = None
        self._vertical_mirror_score = None

    @property
    def transposed(self) -> List[str]:
        if self._transposed is None:
            self._transposed = []
            for row_index in range(len(self._notes[0])):
                self._transposed.append(''.join([_[row_index] for _ in self._notes]))
        return self._transposed

    @property
    def score(self):
        if self._horizontal_mirror_score is None:
            self._horizontal_mirror_score = self.find_horizontal_mirror(self._notes, 0)

        if self._vertical_mirror_score is None:
            self._vertical_mirror_score = self.find_horizontal_mirror(self.transposed, 0)

        return 100 * self._horizontal_mirror_score + self._vertical_mirror_score

    @property
    def smudge_score(self):
        if self._horizontal_mirror_score is None:
            self._horizontal_mirror_score = self.find_horizontal_mirror(self._notes, 1)

        if self._horizontal_mirror_score:
            return 100 * self._horizontal_mirror_score

        if self._vertical_mirror_score is None:
            self._vertical_mirror_score = self.find_horizontal_mirror(self.transposed, 1)

        return self._vertical_mirror_score

    @staticmethod
    def check_candidate(candidate: int, notes: List[str], allowed_difference: int = 0) -> bool:
        differences = Note.string_difference(notes[candidate], notes[candidate + 1])
        check_range = min(candidate, len(notes) - candidate - 2)
        for index_offset in range(check_range):
            if (left := notes[candidate + index_offset + 2]) != (right := notes[candidate - index_offset - 1]):
                differences += sum(_ != __ for _, __ in zip(left, right))
                if differences > allowed_difference:
                    return False

        return differences == allowed_difference

    @staticmethod
    def string_difference(left: str, right: str):
        return sum(_ != __ for _, __ in zip(left, right))

    @staticmethod
    def find_horizontal_mirror(notes: List[str], allowed_difference: int) -> int:
        candidates = [
            _ for _ in range(len(notes) - 1) if Note.string_difference(notes[_], notes[_ + 1]) <= allowed_difference
        ]
        if candidates:
            for candidate in candidates:
                if Note.check_candidate(candidate, notes, allowed_difference):
                    return candidate + 1
        return 0

    def reset(self):
        self._horizontal_mirror_score = None
        self._vertical_mirror_score = None


def main(filename: str):
    with open(filename, 'r') as _f:
        notebook_string = _f.read()

    notebook = [Note(_) for _ in notebook_string.split('\n\n')]

    _score = 0
    _smudge_score = 0

    for note in notebook:
        _score += note.score
        note.reset()
        _smudge_score += note.smudge_score

    print(_score)
    print(_smudge_score)


if __name__ == '__main__':
    main('./input.txt')
