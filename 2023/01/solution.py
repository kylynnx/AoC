from typing import List, Tuple


def load_config(filename: str) -> List[str]:
    with open(filename, "r") as _f:
        return _f.readlines()


def is_int_castable(digit: str) -> bool:
    try:
        int(digit)
        return True
    except (ValueError, TypeError):
        return False


def recover_config_value(obscured_value: str) -> int:
    digits = [int(_) for _ in obscured_value if is_int_castable(_)]
    config_value = 10 * digits[0] + digits[-1]
    return config_value


def decode_digits(obscured_config: List[str],
                  replacements: List[Tuple[str, str]]) -> List[str]:
    if not replacements:
        return obscured_config

    decoded_digits_config = []

    for obscured_value in obscured_config:
        new_value = obscured_value
        for encoded, decoded in replacements:
            new_value = new_value.replace(encoded, decoded)
        decoded_digits_config.append(new_value)
    return decoded_digits_config


def main_part_one(obscured_config: List[str]) -> int:
    config_value_sum = 0
    for obscured_value in obscured_config:
        config_value_sum += recover_config_value(obscured_value)
    return config_value_sum


def main_part_two(obscured_config: List[str]):
    replacements = [
        ("twone", "21"),
        ("oneight", "18"),
        ("threeight", "38"),
        ("fiveight", "58"),
        ("sevenine", "79"),
        ("eightwo", "82"),
        ("eighthree", "83"),
        ("nineight", "98"),
        ("one", "1"),
        ("two", "2"),
        ("three", "3"),
        ("four", "4"),
        ("five", "5"),
        ("six", "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine", "9")
    ]
    obscured_config = decode_digits(obscured_config, replacements=replacements)
    return main_part_one(obscured_config)


def main(filename: str):
    obscured_config = load_config(filename)
    sum_part_one = main_part_one(obscured_config)
    print(f"Sum of config values {sum_part_one}.")

    sum_part_two = main_part_two(obscured_config)
    print(f"Sum of config values {sum_part_two} including spelled digits.")


if __name__ == '__main__':
    main("./input.txt")
