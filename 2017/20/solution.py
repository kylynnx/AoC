import math
from collections import defaultdict
from itertools import combinations


def solve_quadratic(a: int, b: int, c: int) -> set[int]:
    times = set()
    discriminant = b * b - 4 * a * c

    if a == 0:
        if b != 0:
            times.add(-c // b)

        return times

    if discriminant < 0:
        return times

    elif discriminant == 0:
        solution = - b / (2 * a)

        if 0 < solution == int(solution):
            times.add(solution)

        return times

    discriminant = math.sqrt(discriminant) / (2 * a)
    partial = -b / (2 * a)

    positive = partial + discriminant
    if 0 < positive <= int(positive):
        times.add(int(positive))

    negative = partial - discriminant
    if 0 < negative <= int(negative):
        times.add(int(negative))

    return times


class Vector:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __abs__(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    @classmethod
    def from_string(cls, definition: str):
        x, y, z = definition[3:].split(",")

        return cls(int(x), int(y), int(z))


class Particle:
    def __init__(self, idx: int, definition: str):
        self.idx = idx

        pos_def, vel_def, accel_def = definition[:-1].split(">, ")
        self.position = Vector.from_string(pos_def)
        self.velocity = Vector.from_string(vel_def)
        self.acceleration = Vector.from_string(accel_def)

    def move(self):
        self.velocity += self.acceleration
        self.position += self.velocity

    def get_position_at_time(self, t: int) -> Vector:
        """
        Note

        t | v      | x
        --------------------------
        0 | v      | p
        1 | v + a  | p + v + a
        2 | v + 2a | p + 2v + 3a
        3 | v + 3a | p + 3v + 6a


        which can be reduced to x = p + vt + a * (t * t + t) / 2
        """
        t2 = ((t * t) + t) // 2
        return Vector(
            x=self.position.x + self.velocity.x * t + t2 * self.acceleration.x,
            y=self.position.y+ self.velocity.y * t + t2 * self.acceleration.y,
            z=self.position.z+ self.velocity.z * t + t2 * self.acceleration.z,
        )

    def __lt__(self, other):
        if abs(self.acceleration) != abs(other.acceleration):
            return abs(self.acceleration) < abs(other.acceleration)

        if abs(self.velocity) != abs(self.acceleration):
            return abs(self.velocity) < abs(self.acceleration)

        return abs(self.position) < abs(self.acceleration)

    def collides_with(self, other) -> int | None:
        delta_a = self.acceleration.x - other.acceleration.x
        delta_v = self.velocity.x - other.velocity.x
        delta_p = self.position.x - other.position.x
        collision_times = solve_quadratic(a=delta_a, b=delta_a + 2 * delta_v, c=2 * delta_p)

        if collision_times is not None:
            for collision_time in collision_times:
                if other.get_position_at_time(collision_time) == self.get_position_at_time(collision_time):
                    return collision_time

        return None


def main(filename: str):
    with open(filename) as f:
        particles = [Particle(idx=idx, definition=_.strip()) for idx, _ in enumerate(f.readlines())]

    particles.sort()  # For large times acceleration dominates, followed by velocity, followed by position

    min_distance_particle = particles[0].idx
    print(f"In the long term particle {min_distance_particle} will be closest to the origin.")

    collisions = defaultdict(list)

    for one, two in combinations(particles, 2):
        if (collision_time := one.collides_with(two)) is not None:
            collisions[collision_time].append((one.idx, two.idx))

    collision_times = sorted(list(collisions.keys()))
    particles = {_.idx: _ for _ in particles}
    particles_exist = [True] * len(particles)

    while collision_times:
        collision_time = collision_times.pop(0)
        new_particles_exist = [_ for _ in particles_exist]

        collision_pairs = collisions[collision_time]

        for one_idx, two_idx in collision_pairs:
            if particles_exist[one_idx] and particles_exist[two_idx]:
                new_particles_exist[one_idx] = False
                new_particles_exist[two_idx] = False

        particles_exist = new_particles_exist

    print(f"After all collisions are resolved {sum(particles_exist)} particles are left.")


if __name__ == "__main__":
    main("test_part_one.txt")
    main("test_part_two.txt")
    main("input.txt")
