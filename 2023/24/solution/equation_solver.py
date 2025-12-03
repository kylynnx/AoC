from sympy import symbols, solve

from trajectory import Trajectory


class EquationSolver:
    x, y, z = symbols('x,y,z')
    vx, vy, vz = symbols('vx,vy,vz')

    @classmethod
    def get_by_name(cls, name: str):
        match name:
            case 'x':
                return cls.x
            case 'y':
                return cls.y
            case 'z':
                return cls.z
            case 'vx':
                return cls.vx
            case 'vy':
                return cls.vy

        return cls.vz

    @classmethod
    def _get_equation(cls, trajectory_one: Trajectory, trajectory_two: Trajectory, dim_one: str, dim_two: str):
        return (
                (
                    (trajectory_one.velocity.get_by_name(dim_two) - trajectory_two.velocity.get_by_name(dim_two))
                    * cls.get_by_name(dim_one)
                )
                + (
                    (trajectory_two.velocity.get_by_name(dim_one) - trajectory_one.velocity.get_by_name(dim_one))
                    * cls.get_by_name(dim_two)
                )
                + (
                    (trajectory_two.position.get_by_name(dim_two) - trajectory_one.position.get_by_name(dim_two))
                    * cls.get_by_name(f'v{dim_one}')
                )
                + (
                    (trajectory_one.position.get_by_name(dim_one) - trajectory_two.position.get_by_name(dim_one))
                    * cls.get_by_name(f'v{dim_two}')
                )
                - trajectory_one.position.get_by_name(dim_one) * trajectory_one.velocity.get_by_name(dim_two)
                + trajectory_two.position.get_by_name(dim_one) * trajectory_two.velocity.get_by_name(dim_two)
                - trajectory_two.position.get_by_name(dim_two) * trajectory_two.velocity.get_by_name(dim_one)
                + trajectory_one.position.get_by_name(dim_two) * trajectory_one.velocity.get_by_name(dim_one)
        )

    @classmethod
    def solve(cls, trajectory_i: Trajectory, trajectory_j: Trajectory, trajectory_k: Trajectory):
        equations = [
            cls._get_equation(trajectory_one=trajectory_i, trajectory_two=trajectory_j, dim_one='x', dim_two='y'),
            cls._get_equation(trajectory_one=trajectory_i, trajectory_two=trajectory_k, dim_one='x', dim_two='y'),
            cls._get_equation(trajectory_one=trajectory_i, trajectory_two=trajectory_j, dim_one='x', dim_two='z'),
            cls._get_equation(trajectory_one=trajectory_i, trajectory_two=trajectory_k, dim_one='x', dim_two='z'),
            cls._get_equation(trajectory_one=trajectory_i, trajectory_two=trajectory_j, dim_one='y', dim_two='z'),
            cls._get_equation(trajectory_one=trajectory_i, trajectory_two=trajectory_k, dim_one='y', dim_two='z'),
        ]

        solutions = solve(equations, [cls.x, cls.y, cls.z, cls.vx, cls.vy, cls.vz], dict=True)

        return solutions[0]
