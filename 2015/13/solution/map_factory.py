import re

from happiness_map import HappinessMap


class HappinessMapFactory:
    @staticmethod
    def create(filename: str) -> HappinessMap:
        with open(filename) as f:
            happy_strings = [_.strip("\n") for _ in f.readlines()]

        happy = HappinessMap()

        for happy_string in happy_strings:
            left, right, happiness_change = HappinessMapFactory.deserialize(happy_string)
            happy.add_happiness_change(left=left, right=right, change=happiness_change)

        return happy

    @staticmethod
    def deserialize(content: str) -> (str, str, int):
        left = re.search(r"([A-Za-z]+) would", content).group(1)
        right = re.search(r"to ([A-Za-z]+)", content).group(1)
        change_sign = -1 if "lose" in content else 1
        change_value = int(re.search(r"(\d+)", content).group(1))

        return left, right, change_sign * change_value

    @staticmethod
    def add_host(hostname: str, happiness_map: HappinessMap):
        current_people = set(happiness_map.people)
        for person in current_people:
            happiness_map.add_happiness_change(person, hostname, 0)
            happiness_map.add_happiness_change(hostname, person, 0)
