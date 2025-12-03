import hashlib


def get_hash(to_hash: str) -> str:
    return hashlib.md5(to_hash.encode("ascii")).hexdigest()


def main(input_cipher: str, goal_start: str = "00000"):
    result = 0
    found_hash = "notAHash"

    while not found_hash.startswith(goal_start):
        result += 1
        found_hash = get_hash(f"{input_cipher}{result}")

    print(result)


if __name__ == "__main__":
    main(input_cipher="yzbqklnj")
    main(input_cipher="yzbqklnj", goal_start="000000")
