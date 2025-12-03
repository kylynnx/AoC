from elements import Coordinate, Directions
from element_array import ElementArray


def main(filename: str):
    _energy_levels = []
    array = ElementArray(filename=filename)

    for index_x in range(1, array.dim_x - 1):
        array.propagate_beam(
            entry_point=Coordinate(x=index_x, y=1),
            entry_direction=Directions.DOWN
        )
        _energy_levels.append(array.energization)
        array.reset()

        array.propagate_beam(
            entry_point=Coordinate(x=index_x, y=array.dim_y - 2),
            entry_direction=Directions.UP
        )
        _energy_levels.append(array.energization)
        array.reset()

    for index_y in range(1, array.dim_y - 1):
        array.propagate_beam(
            entry_point=Coordinate(x=1, y=index_y),
            entry_direction=Directions.RIGHT
        )
        _energy_levels.append(array.energization)
        array.reset()

        array.propagate_beam(
            entry_point=Coordinate(x=array.dim_x - 2, y=index_y),
            entry_direction=Directions.LEFT
        )
        _energy_levels.append(array.energization)
        array.reset()

    print(max(_energy_levels))


if __name__ == '__main__':
    main(filename='../input.txt')
