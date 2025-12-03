def get_next_code(current_code: int):
    return (current_code * 252533) % 33554393


def main(start: int, row: int, column: int):
    number_of_codes = sum(range(row + column - 1)) + column

    current_code = start

    for _ in range(number_of_codes - 1):
        current_code = get_next_code(current_code)

    print(current_code)


if __name__ == '__main__':
    main(start=20151125, row=2947, column=3029)
