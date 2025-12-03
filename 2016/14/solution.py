import re
from hashlib import md5


quintets = {_: _ * 5 for _ in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]}


def get_hash_string(salt: str, idx: int) -> str:
    return md5(f"{salt}{idx}".encode("utf-8")).hexdigest()


def stretch_hash(hash_string: str) -> str:
    for _ in range(2016):
        hash_string = md5(hash_string.encode("utf-8")).hexdigest()

    return hash_string


def setup_hashmap(salt: str, length: int, use_stretching: bool = False):
    hashmap = [get_hash_string(salt=salt, idx=_) for _ in range(length + 1)]

    if use_stretching:
        hashmap = [stretch_hash(_) for _ in hashmap]

    return hashmap


def main(salt: str, use_stretching: bool = False):
    found_one_time_pads = []
    idx = 0
    hashes = setup_hashmap(salt=salt, length=1000, use_stretching=use_stretching)

    while len(found_one_time_pads) < 64:
        current_hash = hashes.pop(0)

        triplet = re.search(r"(.)\1\1", current_hash)
        if triplet:
            target_string = quintets[triplet.group(1)]
            if any(target_string in _ for _ in hashes):
                found_one_time_pads.append(idx)

        idx += 1
        next_hash = get_hash_string(salt=salt, idx=idx + len(hashes))
        if use_stretching:
            next_hash = stretch_hash(next_hash)
        hashes.append(next_hash)

    print(f"The index searched for is {found_one_time_pads[-1]}.")


if __name__ == '__main__':
    main("jlmsuwbz")
    main("jlmsuwbz", use_stretching=True)
