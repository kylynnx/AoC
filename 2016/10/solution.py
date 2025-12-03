import re
from collections import defaultdict
from enum import Enum

type action_type =  tuple[int, int]
type actions_type = dict[int, tuple[action_type, actions_type]]
type chips_type = dict[int, set[int]]


class OutputType(Enum):
    BOT = "bot"
    OUTPUT = "output"


def main(filename: str):
    with open(filename) as f:
        instructions = [_.strip("\n") for _ in f.readlines()]

    bot_count = get_bot_count(instructions)

    chips = get_starting_values(instructions)
    acting_bots = [k for k, v in chips.items() if len(v) > 1]

    actions = get_bot_actions(instructions)

    if len(actions) != bot_count:
        print("Mismatch of bots and instructions!!")
        return

    target_chips = {17, 61}
    target_id = -1
    bot_found = False
    outputs = dict()

    while acting_bots:
        for bot in acting_bots:
            bot_chips = chips[bot]
            chips[bot] = set()
            if not bot_found and bot_chips == target_chips:
                target_id = bot
                bot_found = True

            low_action, high_action = actions[bot]
            low_value = min(bot_chips)
            high_value = max(bot_chips)
            handle_action(action=low_action, value=low_value, chips=chips, outputs=outputs)
            handle_action(action=high_action, value=high_value, chips=chips, outputs=outputs)
        acting_bots = [k for k, v in chips.items() if len(v) > 1]

    print(f"Bot {target_id} handles chips {target_chips}.")
    print(f"The result ouf outputs is {outputs[0] * outputs[1] * outputs[2]}.")


def get_bot_count(instructions: list[str]) -> int:
    bot_ids = set()

    for instruction in instructions:
        bots = re.findall(r"bot (\d+)", instruction)
        for bot in bots:
            bot_ids.add(int(bot))

    return len(bot_ids)


def get_starting_values(instructions) -> chips_type:
    value_instructions = [_ for _ in instructions if _.startswith("value")]
    starting_chips = defaultdict(set)
    for instruction in value_instructions:
        match = re.match(r"value (\d+) goes to bot (\d+)", instruction)
        bot_id = int(match.group(2))
        value = int(match.group(1))
        starting_chips[bot_id].add(value)

    return starting_chips


def get_bot_actions(instructions):
    action_instructions = [_ for _ in instructions if "gives" in _]

    bot_actions = {}
    for instruction in action_instructions:
        match = re.match(r"bot (\d+) gives low to ([a-z]+) (\d+) and high to ([a-z]+) (\d+)", instruction)
        actor_id = int(match.group(1))
        low_type = OutputType(match.group(2))
        low_id = int(match.group(3))
        high_type = OutputType(match.group(4))
        high_id = int(match.group(5))
        bot_actions[actor_id] = ((low_type, low_id), (high_type, high_id))

    return bot_actions


def handle_action(action: action_type, value: int, chips: chips_type, outputs: dict[int, int]):
    target_type, target_id = action

    if target_type is OutputType.OUTPUT:
        outputs[target_id] = value
        return

    chips[target_id].add(value)


if __name__ == '__main__':
    main("input.txt")
