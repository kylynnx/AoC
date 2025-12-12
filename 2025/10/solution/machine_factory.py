from button import Button
from lights import Lights
from machine import Machine


class MachineFactory:
    @staticmethod
    def build(description: str) -> Machine:
        lights_description, *button_descriptions, joltages_description = description.split(" ")

        lights = MachineFactory._load_lights(lights_description)
        joltages = [int(_) for _ in joltages_description.strip("{").strip("}").split(",")]
        buttons = MachineFactory._load_buttons(button_descriptions)

        return Machine(lights=lights, buttons=buttons, joltages=joltages)

    @staticmethod
    def _load_lights(lights_description: str) -> Lights:
        values = [_ == "#" for _ in lights_description[1:-1]]

        return Lights(values=values)

    @staticmethod
    def _load_buttons(button_descriptions: list[str]) -> list[Button]:
        return [MachineFactory._load_button(_) for _ in button_descriptions]

    @staticmethod
    def _load_button(button_description: str) -> Button:
        toggles = {int(_) for _ in button_description.strip("(").strip(")").split(",")}

        return Button(toggles=toggles)
