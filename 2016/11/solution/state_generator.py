from building_state import BuildingState, check_floor_safe


def get_next_states(state: BuildingState) -> list[BuildingState]:
    current_floor = state.floors[state.elevator_floor]
    next_states = list()
    for moving_generators, moving_microchips in current_floor.combinations():
        for floor in [state.elevator_floor - 1, state.elevator_floor + 1]:
            if  floor < state.minimal_floor or floor >= 4 :
                continue
            target_floor = state.floors[floor]
            if check_floor_safe(
                generators=target_floor.generators.union(moving_generators),
                microchips=target_floor.microchips.union(moving_microchips),
            ):
                new_floors = [_.copy() for _ in state.floors]
                new_floors[floor].generators.update(moving_generators)
                new_floors[floor].microchips.update(moving_microchips)
                new_floors[state.elevator_floor].generators -= moving_generators
                new_floors[state.elevator_floor].microchips -= moving_microchips

                min_floor = -1
                while min_floor < 3 and new_floors[min_floor + 1].is_empty:
                    min_floor += 1

                new_state = BuildingState(
                    floors=new_floors,
                    elevator_floor=floor,
                    minimal_floor=max(min_floor, 0),
                    moves=state.moves + 1,
                )

                next_states.append(new_state)

    return next_states
