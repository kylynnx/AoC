from functools import cmp_to_key

from package_checker import PackageChecker
from package_factory import PackageFactory
from package_pair import PackagePair


def main_one(filename: str):
    with open(filename, 'r') as _f:
        package_pairs = [PackagePair(_) for _ in _f.read().split('\n\n')]

    ordered_pairs = []
    for i in range(len(package_pairs)):
        if PackageChecker.check_order(package_pairs[i]) == 1:
            ordered_pairs.append(i+1)

    print(sum(ordered_pairs))


def main_two(filename: str):
    two_package, _ = PackageFactory.deserialize_package('[2]]')
    six_package, _ = PackageFactory.deserialize_package('[6]]')
    all_packages = [
        two_package,
        six_package
    ]

    with open(filename, 'r') as _f:
        raw_content = _f.read()

    raw_content = raw_content.replace('\n\n', '\n')
    raw_packages = raw_content.split('\n')

    for raw_package in raw_packages:
        package, _ = PackageFactory.deserialize_package(raw_package[1:])
        all_packages.append(package)

    sorted_packages = sorted(all_packages, key=cmp_to_key(PackageChecker.check_left_right), reverse=True)
    print((sorted_packages.index(two_package) + 1) * (sorted_packages.index(six_package) + 1))


def main(filename: str):
    main_one(filename)
    main_two(filename)


if __name__ == '__main__':
    main('../input.txt')
