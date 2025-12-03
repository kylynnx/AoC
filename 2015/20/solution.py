from math import sqrt


def get_divisors(number: int):
    small_divisors = [_ for _ in range(1, int(sqrt(number)) + 1) if number % _ == 0]
    large_divisors = [number / _ for _ in small_divisors if number != _ * _]
    return small_divisors + large_divisors

def part_one(presents: int):
    target = presents // 10
    divisor_sum = 0
    house_number = 0

    while divisor_sum <= target:
        house_number += 1
        divisor_sum = sum(get_divisors(house_number))

    return house_number


def part_two(presents: int, start: int):
    house_number = 831600
    divisor_sum = 0
    while divisor_sum < presents:
        house_number += 1
        divisor_sum = sum(_ for _ in get_divisors(house_number) if house_number / _ <= 50) * 11

    print(house_number)


def main(presents: int):
    start_two = part_one(presents)
    print(start_two)
    part_two(presents, start=start_two)


if __name__ == "__main__":
    main(36000000)
