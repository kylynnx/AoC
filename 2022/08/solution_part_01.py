from typing import Set, Tuple, List


def rotate(tree_lines: List[str]) -> List[str]:
    rotated_tree_lines = []
    for row in range(len(tree_lines)):
        rotated_tree_lines.append(''.join(_[row] for _ in tree_lines))

    return rotated_tree_lines


def check_visibility(tree_line: str, y: int, visible_trees: Set[Tuple[int, int]], invert_xy: bool,
                     invert_x: bool = False) -> Set[Tuple[int, int]]:
    current_x = 0
    max_height = -1
    for tree in tree_line:
        current_tree = int(tree)
        if current_tree > max_height:
            if invert_x:
                x = len(tree_line) - current_x - 1
            else:
                x = current_x
            if invert_xy:
                coordinate = (y, x)
            else:
                coordinate = (x, y)
            visible_trees.add(coordinate)
            max_height = current_tree
        current_x += 1

    return visible_trees


def get_visible_trees(tree_line: str, y: int, invert_xy: bool = False) -> Set[Tuple[int, int]]:
    visible_trees = set()
    check_visibility(tree_line=tree_line, y=y, visible_trees=visible_trees, invert_xy=invert_xy)
    check_visibility(tree_line=tree_line[::-1], y=y, visible_trees=visible_trees, invert_xy=invert_xy, invert_x=True)

    return visible_trees


def main(filename: str):
    with open(filename, 'r') as _f:
        tree_lines = [_.strip('\n') for _ in _f.readlines()]

    visible_trees = set()
    current_y = 0
    for tree_line in tree_lines:
        visible_trees = visible_trees.union(get_visible_trees(tree_line, y=current_y))
        current_y += 1

    rotated_tree_lines = rotate(tree_lines)
    current_y = 0
    for tree_line in rotated_tree_lines:
        visible_trees = visible_trees.union(get_visible_trees(tree_line, y=current_y, invert_xy=True))
        current_y += 1

    print(len(visible_trees))


if __name__ == '__main__':
    main('input.txt')
