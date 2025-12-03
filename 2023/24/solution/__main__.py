import itertools
from typing import List

from equation_solver import EquationSolver
from vector import Vector
from trajectory import Trajectory


def load_trajectories(filename: str) -> List[Trajectory]:
    with open(filename, 'r') as _f:
        trajectories = []
        for line in _f.readlines():
            pos_string, vel_string = line.split(' @ ')
            pos_list = [int(_) for _ in pos_string.split(', ')]
            vel_list = [int(_) for _ in vel_string.split(', ')]
            trajectories.append(Trajectory(position=Vector(*pos_list), velocity=Vector(*vel_list)))

    return trajectories


def check_intercept(traj_one: Trajectory, traj_two: Trajectory, lower_bound: float, upper_bound: float) -> bool:
    if traj_one.slope_2d == traj_two.slope_2d:
        return False
    x_intersect = (traj_two.intercept_2d - traj_one.intercept_2d) / (traj_one.slope_2d - traj_two.slope_2d)
    y_intersect = traj_one.get_y(x_intersect)
    t_intersect_one = (x_intersect - traj_one.position.x) / traj_one.velocity.x
    t_intersect_two = (x_intersect - traj_two.position.x) / traj_two.velocity.x

    if (
        not lower_bound <= x_intersect <= upper_bound
        or
        not lower_bound <= y_intersect <= upper_bound
        or
        t_intersect_one < 0
        or
        t_intersect_two < 0
    ):
        return False

    return True


def main_part_one(filename: str, lower_bound: int, upper_bound: int):
    trajectories = load_trajectories(filename)

    crossings = 0

    for a, b in itertools.combinations(trajectories, 2):
        if check_intercept(a, b, lower_bound=lower_bound, upper_bound=upper_bound):
            crossings += 1

    print(crossings)


def main_part_two(filename: str):
    trajectories = load_trajectories(filename)
    solution = EquationSolver.solve(
        trajectory_i=trajectories[0], trajectory_j=trajectories[1], trajectory_k=trajectories[2]
    )

    print(int(solution[EquationSolver.x] + solution[EquationSolver.y] + solution[EquationSolver.z]))


if __name__ == '__main__':
    main_part_one('../input.txt', lower_bound=200000000000000, upper_bound=400000000000000)
    main_part_two('../input.txt')
