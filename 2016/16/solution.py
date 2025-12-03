def main(disk_length: int, initial_state: str):
    data = generate_data(initial_state, disk_length)[:disk_length]
    checksum = calculate_checksum(data)
    print(f"Checksum: {checksum}.")


def calculate_checksum(data: str):
    checksum = ""

    idx = 0
    while idx < len(data):
        if data[idx: idx + 2] in ["00", "11"]:
            checksum += "1"
        else:
            checksum += "0"
        idx += 2

    if len(checksum) % 2 == 0:
        return calculate_checksum(checksum)

    return checksum

def generate_data(initial_state: str, length: int):
    data = initial_state

    while len(data) < length:
        data = generate_data_step(data)

    return data


def generate_data_step(head: str):
    tail = head[::-1].replace("0", "#")
    tail = tail.replace("1", "0")
    tail = tail.replace("#", "1")

    return f"{head}0{tail}"


if __name__ == '__main__':
    main(disk_length=20, initial_state="10000")
    main(disk_length=272, initial_state="11101000110010100")
    main(disk_length=35651584, initial_state="11101000110010100")
