from sensor_array import SensorArray


def main(filename: str, y: int, upper_bound: int):
    sensor_array = SensorArray(filename)
    print(sensor_array.count_forbidden_beacon_positions(y=y))
    beacon_x, beacon_y = sensor_array.find_allowed_beacon_coordinates(lower_bound=0, upper_bound=upper_bound)
    print(beacon_x * 4000000 + beacon_y)


if __name__ == '__main__':
    main('../input.txt', 2000000, 4000000)
