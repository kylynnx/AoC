def main(first_row: str, rows: int):
    safe_tiles = first_row.count(".")
    row_count = 1
    current_row = first_row

    while row_count < rows:
        current_row = get_next_row(row=current_row)
        row_count += 1
        safe_tiles += current_row.count(".")

    print(f"The room has {safe_tiles} safe tiles.")


def get_next_row(row: str) -> str:
    padded_row = f".{row}."
    trap_configurations = [
        "^^.",
        ".^^",
        "^..",
        "..^",
    ]
    next_row=""

    for idx in range(len(row)):
        if padded_row[idx: idx + 3] in trap_configurations:
            next_row += "^"
        else:
            next_row += "."

    return next_row


if __name__ == "__main__":
    main(first_row=".^^.^.^^^^", rows=10)
    main(
        first_row="...^^^^^..^...^...^^^^^^...^.^^^.^.^.^^.^^^.....^.^^^...^^^^^^.....^.^^...^^^^^...^.^^^.^^......^^^^",
        rows=40,
    )
    main(
        first_row="...^^^^^..^...^...^^^^^^...^.^^^.^.^.^^.^^^.....^.^^^...^^^^^^.....^.^^...^^^^^...^.^^^.^^......^^^^",
        rows=400000,
    )
