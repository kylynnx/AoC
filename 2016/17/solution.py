from hashlib import md5


def main(passcode: str, find_longest: bool = False):
    shortest_path = None
    longest_path_length = 0

    directions = [
        ("U", 0, (0, -1)),
        ("D", 1, (0, 1)),
        ("L", 2, (-1, 0)),
        ("R", 3, (1, 0))
    ]

    open_indicators = ["b", "c", "d", "e", "f"]
    target = (3, 3)
    queue = [("", (0, 0))]

    while queue:
        path, position = queue.pop(0)

        if position == target:
            if shortest_path is None:
                shortest_path = path

            if not find_longest:
                break
            elif len(path) > longest_path_length:
                longest_path_length = len(path)
        else:
            hashed = md5(f"{passcode}{path}".encode("utf-8")).hexdigest()
            for name, idx, vector in directions:
                new_x = position[0] + vector[0]
                new_y = position[1] + vector[1]

                if new_x < 0 or new_x > 3 or new_y < 0 or new_y > 3 or hashed[idx] not in open_indicators:
                    continue

                queue.append((path + name, (new_x, new_y)))

    print(f"Passcode: {passcode}:")
    print(f"The shortest path to the target is '{shortest_path}'.")

    if find_longest:
        print(f"The longest path has {longest_path_length} steps.")
    print("")


if __name__ == "__main__":
    main(passcode="ihgpwlah", find_longest=True)  # DDRRRD, 370
    main(passcode="kglvqrro", find_longest=True)  # DDUDRLRRUDRD, 492
    main(passcode="ulqzkmiv", find_longest=True)  # DRURDRUDDLLDLUURRDULRLDUUDDDRR, 830
    main(passcode="qzthpkfp", find_longest=True)
