def main(filename: str, max_value: int):
    with open(filename) as f:
        forbidden_ranges = sorted(
            [tuple(int(_) for _ in __.strip("\n").split("-")) for __ in f.readlines()],
        )

    lowest_allowed_ip = find_lowest_allowed_ip(forbidden_ranges=forbidden_ranges)

    if lowest_allowed_ip is not None:
        print(f"The lowest allowed IP is {lowest_allowed_ip}.")

    blocked_ip_count = count_blocked_ips(forbidden_ranges=forbidden_ranges)
    allowed_ip_count = max_value - blocked_ip_count + 1
    print(f"In total {allowed_ip_count} IPs are allowed.")


def count_blocked_ips(forbidden_ranges):
    blocked_ip_count = 0

    current_min, current_max = forbidden_ranges[0]

    for forbidden_range in forbidden_ranges[1:]:
        if forbidden_range[0] > current_max:
            blocked_ip_count += current_max - current_min + 1
            current_min, current_max = forbidden_range
        elif forbidden_range[0] < current_min:
            current_min = forbidden_range[0]
        elif forbidden_range[1] > current_max:
            current_max = forbidden_range[1]

    blocked_ip_count += current_max - current_min + 1

    return blocked_ip_count



def find_lowest_allowed_ip(forbidden_ranges) -> int | None:
    candidates = [x + 1 for _, x in forbidden_ranges]

    for candidate in candidates:
        if all((start <= candidate <= end )is False for start, end in forbidden_ranges):
            return candidate

    return None


if __name__ == "__main__":
    main(filename="test.txt", max_value=9)
    print("")
    main(filename="input.txt", max_value=4294967295)
