from elements import Coordinate, Directions
from element_array import ElementArray


def main(filename: str):
    array = ElementArray(filename=filename)
    array.propagate_beam(entry_direction=Directions.RIGHT, entry_point=Coordinate(x=1, y=1))
    print(array.energization)


if __name__ == '__main__':
    main('../input.txt')
