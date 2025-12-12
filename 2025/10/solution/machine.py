from heapq import heappush, heappop

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, COIN_CMD
from pulp.apis.coin_api import pulp_cbc_path

from button import Button
from lights import Lights


class Machine:
    def __init__(self, lights: Lights, buttons: list[Button], joltages: list[int]):
        self._lights = lights
        self._buttons = buttons
        self._joltages = joltages
        self._lights_configuration_length = None
        self._joltages_configuration_length = None


    @property
    def lights_configuration_length(self) -> int:
        if self._lights_configuration_length is None:
            self._configure_lights()

        return self._lights_configuration_length

    @property
    def joltages_configuration_length(self) -> int:
        if self._joltages_configuration_length is None:
            self._configure_joltages()

        return self._joltages_configuration_length

    def _configure_lights_slow(self) -> None:
        queue = []
        initial_state = Lights([False] * len(self._lights))
        heappush(queue, (0, self._lights.distance(initial_state), initial_state))
        seen = set()

        while queue:
            presses, _, lights = heappop(queue)
            seen.add(lights)

            if lights == self._lights:
                self._lights_configuration_length = presses
                break

            for button in self._buttons:
                new_lights = button.apply(lights=lights)

                if new_lights in seen:
                    continue

                heappush(queue, (presses + 1, self._lights.distance(new_lights), new_lights))

    def _configure_lights(self) -> None:
        queue = []
        heappush(queue, (0, 0))
        seen = set()

        target_lights = self._lights.numeric
        buttons = [_.numeric for _ in self._buttons]

        while queue:
            presses, lights = heappop(queue)
            if lights in seen:
                continue

            seen.add(lights)

            if lights == target_lights:
                self._lights_configuration_length = presses
                break

            for button in buttons:
                new_lights = lights ^ button

                if new_lights in seen:
                    continue

                heappush(queue, (presses + 1, new_lights))

    def _configure_joltages(self) -> None:
        problem = LpProblem(sense=LpMinimize)

        button_variables = [LpVariable(f"{idx}", lowBound=0, cat="Integer") for idx in range(len(self._buttons))]

        problem += lpSum(button_variables)

        for idx_j, joltage in enumerate(self._joltages):
            problem += (
                lpSum(
                    [_ for idx_b, _ in enumerate(button_variables) if idx_j in self._buttons[idx_b].toggles]
                ) == joltage
            )
        problem.solve(COIN_CMD(msg=False, path=pulp_cbc_path))

        self._joltages_configuration_length = int(problem.objective.value())
