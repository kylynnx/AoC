def find_split_index(value: str) -> list[int]:
    current_digit = value[0]
    indexes = [0]

    for i in range(1, len(value)):
        if value[i] != current_digit:
            indexes.append(i)
            current_digit = value[i]

    indexes.append(len(value))

    return indexes


def step(input_value: str) -> str:
    split_indexes = find_split_index(input_value)

    result = ""
    for i in range(len(split_indexes) - 1):
        count = split_indexes[i + 1] - split_indexes[i]
        digit = input_value[split_indexes[i]]
        result += f"{count}{digit}"

    return result


def part(start_value: str, step_count: int):
    next_step = start_value

    for _ in range(step_count):
        next_step = step(next_step)

    return next_step


def main():
    result_one = part("1321131112", 40)
    print(len(result_one))
    result_two = part(result_one, 10)
    print(len(result_two))


if __name__ == '__main__':
    main()
