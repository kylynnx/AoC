def main(filename: str):
    with open(filename) as f:
        rotations = [_.strip()  for _ in f.readlines()]

    password = 0
    enhanced_password = 0
    dial = 50

    for rotation in rotations:
        direction, distance = read_rotation(rotation=rotation)
        enhanced_password += count_zero_passes(dial=dial, direction=direction, distance=distance)
        dial = rotate_dial(dial=dial, direction=direction, distance=distance)

        if dial == 0:
            password += 1
            enhanced_password += 1

    print(f"The password is {password}.")
    print(f"Using method '0x434C49434B' the password becomes {enhanced_password}.")


def read_rotation(rotation: str) -> tuple[str, int]:
    direction = rotation[0]
    distance = int(rotation[1:])

    return direction, distance


def rotate_dial(dial: int, direction: str, distance: int) -> int:
    if direction == "L":
        distance *= -1

    dial += distance
    dial %= 100

    return dial


def count_zero_passes(dial: int, direction: str, distance: int) -> int:
    zero_passes = distance // 100

    if dial == 0:
        return zero_passes

    remainder = distance % 100

    if direction == "L" and dial - remainder < 0:
        zero_passes += 1

    if direction == "R" and dial + remainder > 100:
        zero_passes += 1

    return zero_passes


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
