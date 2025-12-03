import re
from functools import cmp_to_key


def read_room_name_checksum_and_sector_id(line: str) -> tuple[str, str, int]:
    match = re.match(r"([a-z-]+)-(\d{3})\[([a-z]+)]", line)
    name = match.group(1)
    sector_id = int(match.group(2))
    checksum = match.group(3)

    return name, checksum, sector_id


def sort_key(left: tuple[int, str], right: tuple[int, str]) -> int:
    if left[0] != right[0]:
        return right[0] - left[0]

    return ord(left[1]) - ord(right[1])



def calculate_checksum(name: str) -> str:
    cleaned_name = name.replace("-", "")
    letters = set(_ for _ in cleaned_name)
    count_letters = sorted([(cleaned_name.count(_), _) for _ in letters], key=cmp_to_key(sort_key))
    checksum = "".join([_[1] for _ in count_letters[:5]])
    return checksum

def decrypt(name: str, sector_id: int) -> str:
    decrypted = ""
    offset = sector_id % 26

    for word in name.split("-"):
        for letter in word:
            decrypted_ord = ord(letter) + offset
            if decrypted_ord > ord("z"):
                decrypted_ord -= 26
            decrypted += chr(decrypted_ord)
        decrypted += " "

    return decrypted[:-1]


def main(filename: str):
    with open(filename) as f:
        rooms = [read_room_name_checksum_and_sector_id(_) for _ in f.readlines()]

    id_sum = 0
    real_rooms = []
    for name, checksum, sector_id in rooms:
        if checksum == calculate_checksum(name):
            id_sum += sector_id
            real_rooms.append((name, sector_id))
    print(id_sum)

    for name, sector_id in real_rooms:
        decrypted_name = decrypt(name, sector_id)
        if any(_  in decrypted_name for _ in ("north", "pole", "christmas",)):
            print(f"{decrypted_name} -> {sector_id}")


if __name__ == '__main__':
    main("input.txt")