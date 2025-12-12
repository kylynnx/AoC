from point import Point
from polygon import Polygon


def main(filename: str):
    with open(filename) as f:
        points = [Point(*(int(_) for _ in line.split(","))) for line in f.readlines()]

    polygon = Polygon(points)
    print(f"The largest possible area is {polygon.get_max_area()}.")
    print(f"If only using red and green tiles the size is {polygon.get_max_area(inscribed=True)}.")


if __name__ == "__main__":
    main("../test.txt")
    main("../input.txt")
