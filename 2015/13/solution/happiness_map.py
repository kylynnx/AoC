class HappinessMap:
    def __init__(self):
        self._happiness_changes: dict[str, dict[str, int]] = {}
        self._people: set[str] = set()

    @property
    def people(self) -> set[str]:
        return self._people

    def add_happiness_change(self, left: str, right: str, change: int):
        self._people.add(left)
        self._people.add(right)

        if left not in self._happiness_changes:
            self._happiness_changes[left] = dict()

        self._happiness_changes[left][right] = change

    def get_happiness_change(self, left: str, right: str) -> int:
        return self._happiness_changes[left][right]
