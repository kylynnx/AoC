from typing import List


def determine_item_priority(item) -> int:
    return ord(item.lower()) - ord('a') + 1 + 26 * item.isupper()


def determine_rucksack_priority(rucksack: str) -> int:
    half = len(rucksack) // 2
    first_compartment = set(rucksack[:half])
    second_compartment = set(rucksack[half:])
    faulty_sorted = first_compartment.intersection(second_compartment)

    rucksack_priority = 0
    for item in faulty_sorted:
        rucksack_priority += determine_item_priority(item)

    return rucksack_priority


def determine_group_priority(group: List[str]) -> int:
    rucksack_sets = [set(_) for _ in group]
    badges = set.intersection(*rucksack_sets)

    badge_priority = 0
    for badge in badges:
        badge_priority += determine_item_priority(badge)

    return badge_priority


def main(filename: str):
    with open(filename, 'r') as _f:
        rucksacks = [_.strip('\n') for _ in _f.readlines()]

    priority_sum = 0
    for rucksack in rucksacks:
        priority_sum += determine_rucksack_priority(rucksack)

    print(priority_sum)

    group_index = 0
    grouped_priority = 0
    while group_index < len(rucksacks):
        group = rucksacks[group_index: group_index + 3]
        grouped_priority += determine_group_priority(group)

        group_index += 3

    print(grouped_priority)


if __name__ == '__main__':
    main('input.txt')
