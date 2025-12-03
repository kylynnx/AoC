def calculate_decompressed_length(compressed_content: str, nested_compression: bool = False) -> int:
    compressed_length = len(compressed_content)
    pointer = 0
    decompressed_length = 0

    while pointer in range(compressed_length):
        match compressed_content[pointer]:
            case "(":
                pointer_movement, length_addition = handle_marker(
                    compressed_content[pointer + 1:],
                    nested_compression=nested_compression
                )
                pointer += pointer_movement
                decompressed_length += length_addition
                continue
            case _:
                decompressed_length += 1
                pointer += 1

    return decompressed_length

def handle_marker(compressed_content: str, nested_compression: bool) -> tuple[int, int]:
    letter_count = 0
    pointer_movement = 0
    while compressed_content[pointer_movement] != "x":
        letter_count = 10 * letter_count + int(compressed_content[pointer_movement])
        pointer_movement += 1
    pointer_movement += 1

    multiplicator = 0
    while compressed_content[pointer_movement] != ")":
        multiplicator = multiplicator * 10 + int(compressed_content[pointer_movement])
        pointer_movement += 1
    pointer_movement += 1

    data_section = compressed_content[pointer_movement:pointer_movement + letter_count]
    if nested_compression and "(" in data_section:
        data_length = calculate_decompressed_length(data_section, nested_compression=nested_compression)
    else:
        data_length = letter_count

    pointer_movement += letter_count + 1
    length_addition = data_length * multiplicator
    return pointer_movement, length_addition


def main(filename: str):
    with open(filename) as f:
        compressed_content = f.read()
    decompressed_length = calculate_decompressed_length(compressed_content)
    print(f"The decompressed length is {decompressed_length} using version 1.")
    decompressed_length = calculate_decompressed_length(compressed_content, nested_compression=True)
    print(f"The decompressed length is {decompressed_length} using version 2.")



if __name__ == '__main__':
    main("input.txt")
