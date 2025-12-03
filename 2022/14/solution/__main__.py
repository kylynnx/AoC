from cave import Cave


def main(filename: str):
    cave = Cave(filename)
    cave.fill_bottomless()
    print(cave.sand_count - 1)
    cave.fill()
    print(cave.sand_count)


if __name__ == "__main__":
    main('../input.txt')
