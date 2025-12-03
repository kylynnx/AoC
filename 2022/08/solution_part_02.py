from solution_part_01 import rotate


def get_vision_length(tree_height: int, partial_line: str) -> int:
    vision_length = 1
    while vision_length < len(partial_line) and int(partial_line[vision_length - 1]) < tree_height:
        vision_length += 1

    return vision_length


def get_scenic_score(index_tree: int, tree_line: str, index_rotated_tree: int, rotated_tree_line: str):
    if index_tree in [0, len(tree_line) - 1] or index_rotated_tree in [0, len(rotated_tree_line) - 1]:
        return 0

    tree_height = int(tree_line[index_tree])

    left_vision = get_vision_length(tree_height=tree_height, partial_line=tree_line[:index_tree][::-1])
    right_vision = get_vision_length(tree_height=tree_height, partial_line=tree_line[index_tree + 1:])
    up_vision = get_vision_length(tree_height=tree_height, partial_line=rotated_tree_line[:index_rotated_tree][::-1])
    down_vision = get_vision_length(tree_height=tree_height, partial_line=rotated_tree_line[index_rotated_tree + 1:])

    return left_vision * right_vision * up_vision * down_vision


def main(filename: str):
    with open(filename, 'r') as _f:
        tree_lines = [_.strip('\n') for _ in _f.readlines()]

    rotated_tree_lines = rotate(tree_lines)
    tree_lines_length = len(tree_lines)
    tree_line_length = len(tree_lines[0])

    scenic_scores = set()

    current_y = 0
    while current_y < tree_lines_length:
        current_x = 0
        while current_x < tree_line_length:
            scenic_scores.add(
                get_scenic_score(
                    index_tree=current_x, tree_line=tree_lines[current_y],
                    index_rotated_tree=current_y, rotated_tree_line=rotated_tree_lines[current_x]
                )
            )
            current_x += 1
        current_y += 1

    print(max(scenic_scores))


if __name__ == '__main__':
    main('input.txt')
