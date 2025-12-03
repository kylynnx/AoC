from package_factory import PackageFactory


class PackagePair:
    def __init__(self, package_pair_string: str):
        left_string, right_string = package_pair_string.split('\n')

        self._left, _ = PackageFactory.deserialize_package(left_string[1:])
        self._right, _ = PackageFactory.deserialize_package(right_string[1:])

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right
