import re
import string
from itertools import combinations

abba_partials = None
bab_partials = None


def get_abba_partials():
    global abba_partials
    if abba_partials is None:
        abba_combinations = list(combinations(string.ascii_lowercase, 2))
        abba_combinations += [(_[1], _[0]) for _ in abba_combinations]
        abba_combinations = ["".join(_) for _ in abba_combinations]
        abba_partials = [f"{_}{_[::-1]}" for _ in abba_combinations]

    return abba_partials


def get_bab_partials():
    global bab_partials

    if bab_partials is None:
        bab_combinations = list(combinations(string.ascii_lowercase, 2))
        bab_combinations += [(_[1], _[0]) for _ in bab_combinations]
        bab_combinations = ["".join(_) for _ in bab_combinations]
        bab_partials = [f"{_}{_[0]}" for _ in bab_combinations]

    return bab_partials


def contains_abba(partial_ip: str) -> bool:
    return any(_ in partial_ip for _ in get_abba_partials())


def split_ip(ip: str) -> tuple[set[str], set[str]]:
    partials = re.findall(r"[a-z]+\[[a-z]+]", ip)
    final_partial = re.search(r"]([a-z]+)$", ip).group(1)
    outside_partials = set()
    inside_partials = set()

    for partial in partials:
        match = re.search(r"([a-z]+)\[([a-z]+)]", partial)
        outside_partials.add(match.group(1))
        inside_partials.add(match.group(2))

    outside_partials.add(final_partial)
    return outside_partials, inside_partials


def supports_tls(ip: str) -> bool:
    outside_partials, inside_partials = split_ip(ip)

    return any(contains_abba(_) for _ in outside_partials) and all(not contains_abba(_) for _ in inside_partials)


def supports_ssl(ip: str) -> bool:
    outside_partials, inside_partials = split_ip(ip)

    outside_aba = [_ for partial in outside_partials for _ in get_bab_partials() if _ in partial]
    inside_bab = [_ for partial in inside_partials for _ in get_bab_partials() if _ in partial]
    return len(set(_ for _ in outside_aba if f"{_[1]}{_[:-1]}" in inside_bab)) > 0


def main(filename: str):
    with open(filename) as f:
        ips = [_.strip("\n") for _ in f.readlines()]

    count_tls_ips = 0
    count_ssl_ips = 0
    for ip in ips:
        count_tls_ips += supports_tls(ip)
        count_ssl_ips += supports_ssl(ip)

    print(f"Part 1: {count_tls_ips}")
    print(f"Part 2: {count_ssl_ips}")


if __name__ == '__main__':
    main("input.txt")
