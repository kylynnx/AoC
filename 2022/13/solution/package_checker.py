from package_pair import PackagePair


class PackageChecker:
    @staticmethod
    def check_order(package_pair: PackagePair) -> int:
        return PackageChecker.check_left_right(package_pair.left, package_pair.right)

    @staticmethod
    def compare_ints(left: int, right: int) -> int:
        if left < right:
            return 1
        elif left == right:
            return 0

        return -1

    @staticmethod
    def check_left_right(left, right):
        if isinstance(left, int) and isinstance(right, int):
            return PackageChecker.compare_ints(left, right)

        if not isinstance(left, list):
            left = [left]

        if not isinstance(right, list):
            right = [right]

        min_len = min(len(left), len(right))

        for i in range(min_len):
            res = PackageChecker.check_left_right(left[i], right[i])
            if res == -1:
                return -1
            elif res == 1:
                return 1

        return PackageChecker.compare_ints(len(left), len(right))
