from typing import List, Tuple


class PackageFactory:
    @staticmethod
    def deserialize_package(package_string: str) -> Tuple[List[int], int]:
        cursor = 0
        current_list = []

        while cursor < len(package_string):
            current_number = ''
            next_part = ''
            while next_part not in [',', '[', ']']:
                current_number += next_part
                next_part = package_string[cursor]
                cursor += 1

            match next_part:
                case ',':
                    if current_number:
                        current_list.append(int(current_number))
                case '[':
                    sub_list, cursor_delta = PackageFactory.deserialize_package(package_string[cursor:])
                    current_list.append(sub_list)
                    cursor += cursor_delta
                case ']':
                    if current_number:
                        current_list.append(int(current_number))
                    return current_list, cursor
