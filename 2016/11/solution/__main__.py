from building_state import BuildingState
from state_generator import get_next_states


def find_number_of_steps(start_state: BuildingState) -> int:
    seen_states = set()

    states = [start_state]
    final_state = None

    while states:
        current_state = states.pop(0)
        if current_state.id in seen_states:
            continue

        seen_states.add(current_state.id)

        if current_state.assembled:
            final_state = current_state
            break

        states += get_next_states(current_state)

    return final_state.moves


def main(filename: str):
    start_state = BuildingState.from_file(filename=filename)
    moves = find_number_of_steps(start_state)
    print(f"It takes {moves} moves.")

    next_floors = [_.copy() for _ in start_state.floors]
    next_floors[0].generators.update({"elerium", "dilithium"})
    next_floors[0].microchips.update({"elerium", "dilithium"})
    next_start = BuildingState(
        floors=next_floors,
        elevator_floor=0,
        minimal_floor=0,
        moves=0,
    )
    moves = find_number_of_steps(next_start)
    print(f"It takes {moves} moves with the additional parts.")


if __name__ == '__main__':
    main("../input.txt")
