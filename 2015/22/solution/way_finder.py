from heapq import heappush, heappop

from game_state import GameState

def find_least_mana_win(initial_state: GameState) -> GameState:
    queue:list[GameState] = []

    _, starting_states = initial_state.get_next_states()

    for state in starting_states:
        heappush(queue, state)

    while queue:
        current_state = heappop(queue)

        if won_lost := current_state.boss_turn():
            return current_state

        elif won_lost is None:
            won, next_states = current_state.get_next_states()

            if won:
                return current_state

            for state in next_states:
                heappush(queue, state)

    raise ValueError("Player cannot win")
