from point import Point


class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.min_x = min(start.x, end.x)
        self.max_x = max(start.x, end.x)
        self.min_y = min(start.y, end.y)
        self.max_y = max(start.y, end.y)

    @property
    def points(self) -> set[Point]:
        points = set()
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                points.add(Point(x, y))
        return points

    def __contains__(self, item: Point) -> bool:
        return self.min_x < item.x < self.max_x and self.min_y < item.y < self.max_y
