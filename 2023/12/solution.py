from enum import Enum
from functools import cache
from typing import Tuple


class SpringState(Enum):
    OPERATIONAL = '.'
    DAMAGED = '#'
    UNKNOWN = '?'


def unfold(springs: str, damaged_groups: Tuple[int, ...], factor: int = 5) -> Tuple[str, Tuple[int, ...]]:
    springs = '?'.join(springs for _ in range(factor))
    new_groups = ()
    for i in range(factor):
        new_groups += damaged_groups

    return springs, new_groups


@cache
def check_string(springs: str, damaged_groups: Tuple[int, ...], current_group_length: int):
    if not springs:
        if len(damaged_groups) > 1:
            return 0

        if (damaged_groups and current_group_length == damaged_groups[0]) or not damaged_groups:
            return 1

        return 0
    if not damaged_groups and SpringState.DAMAGED.value in springs:
        return 0

    match springs[0]:
        case SpringState.OPERATIONAL.value:
            if current_group_length:
                if current_group_length < damaged_groups[0]:
                    return 0
                damaged_groups = damaged_groups[1:]

            return check_string(springs[1:], damaged_groups=damaged_groups, current_group_length=0)
        case SpringState.DAMAGED.value:
            current_group_length += 1
            if current_group_length > damaged_groups[0]:
                return 0

            return check_string(springs[1:], damaged_groups=damaged_groups, current_group_length=current_group_length)
        case SpringState.UNKNOWN.value:
            return (
                check_string(
                    springs=SpringState.OPERATIONAL.value + springs[1:],
                    damaged_groups=damaged_groups,
                    current_group_length=current_group_length
                )
                +
                check_string(
                    springs=SpringState.DAMAGED.value + springs[1:],
                    damaged_groups=damaged_groups,
                    current_group_length=current_group_length
                )
            )


def main(filename: str):
    with open(filename, 'r') as _f:
        record_lines = _f.readlines()

    _combinations = 0
    _unfolded_combinations = 0

    for record in record_lines:
        spring_string, damaged_groups_string = record.split(' ')
        damaged_groups = tuple(int(_) for _ in damaged_groups_string.split(','))
        _combinations += check_string(spring_string, damaged_groups, 0)
        unfolded_string, unfolded_groups = unfold(spring_string, damaged_groups)
        _unfolded_combinations += check_string(unfolded_string, unfolded_groups, 0)

    print(_combinations)
    print(_unfolded_combinations)


if __name__ == '__main__':
    main('./input.txt')
