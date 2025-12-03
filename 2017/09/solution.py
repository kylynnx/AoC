def find_garbage(stream) -> tuple[int, str]:
    garbage = "<"
    idx = 0
    garbage_length = 0

    while idx < len(stream):
        match (char := stream[idx]):
            case ">":
                garbage += char
                break
            case "!":
                garbage += char
                garbage += stream[idx + 1]
                idx += 1
            case _:
                garbage += char
                garbage_length += 1
        idx += 1

    return garbage_length, garbage


def get_stream_score(stream: str, parent_score: int = -1) -> tuple[int, str, int]:
    max_idx = len(stream)
    idx = 0
    group = ""
    group_score = parent_score + 1
    total_garbage_length = 0

    while idx < max_idx:
        match (char := stream[idx]):
            case '<':
                garbage_length, garbage = find_garbage(stream[idx + 1:])
                idx += len(garbage)
                group += garbage
                total_garbage_length += garbage_length
            case "{":
                subscore, subgroup, sub_garbage_length = get_stream_score(stream[idx + 1:], parent_score=parent_score + 1)
                subgroup = "{" + subgroup
                idx += len(subgroup)
                group += subgroup
                group_score += subscore
                total_garbage_length += sub_garbage_length
            case "}":
                group += "}"
                return group_score, group, total_garbage_length
            case "!":
                group += stream[idx:idx + 2]
                idx = idx + 2
            case _:
                group += char
                idx = idx + 1

    return group_score, group, total_garbage_length


def main(filename: str):
    with open(filename) as f:
        character_stream = f.read().strip()

    score, _, garbage_length = get_stream_score(character_stream)

    print(f"The total score of the input is {score}. It contains {garbage_length} characters of garbage.")


if __name__ == "__main__":
    score_test_cases = [
        ("{}", 1),
        ("{{{}}}", 6),
        ("{{{},{},{{}}}}", 16),
        ("{<a>,<a>,<a>,<a>}", 1),
        ("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
        ("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
        ("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3),
    ]

    for test_stream, expected_score in score_test_cases:
        test_score, _, _ = get_stream_score(test_stream)

        assert test_score == expected_score

    garbage_test_cases = [
        (">", 0),
        ("random characters>", 17),
        ("<<<>", 3),
        ("{!>}>", 2),
        ("!!>", 0),
        ("!!!>>", 0),
        ("{o\"i!a,<{i<a>", 10),
    ]

    for test_garbage, expected_length in garbage_test_cases:
        test_length, _ = find_garbage(test_garbage)
        assert test_length == expected_length

    main("input.txt")
