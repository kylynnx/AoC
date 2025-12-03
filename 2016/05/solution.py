from hashlib import md5


def find_password_in_order(door_id: str):
    password = ""

    index = 0
    while len(password) < 8:
        hash_value = md5(f"{door_id}{index}".encode("utf-8")).hexdigest()

        if hash_value.startswith("00000"):
            password += hash_value[5]

        index += 1

    return password


def find_password_without_order(door_id: str):
    password: list[str] = ["_"] * 8

    index = 0
    password_count = 0
    while password_count < 8:
        hash_value = md5(f"{door_id}{index}".encode("utf-8")).hexdigest()

        if hash_value.startswith("00000") and hash_value[5] in ["0", "1", "2", "3", "4", "5", "6", "7"]:
            password_index = int(hash_value[5])

            if password[password_index] == "_":
                password[password_index] = hash_value[6]
                password_count += 1

        index += 1

    return "".join(password)

def main(door_id: str):
    print(find_password_in_order(door_id))
    print(find_password_without_order(door_id))


if __name__ == "__main__":
    main("wtnhxymk")
