import re


def main():
    initial_value = 1
    constant = 14 * 182

    while True:
        if re.match(r"^0b(10)+$", bin(initial_value + constant)):
            break
        initial_value += 1

    print(f"The smallest positive integer to achieve the clock signal is {initial_value}.")



if __name__ == "__main__":
    main()
