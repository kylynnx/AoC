def main(filename: str):
    with open(filename) as f:
        banks = [int(_) for _ in f.read().split("\t")]

    seen_states = set()
    state_map = {}
    current_state = banks
    steps = 0

    while (tpl_cur := tuple(current_state))not in seen_states:
        state_map[tpl_cur] = steps
        seen_states.add(tpl_cur)
        steps += 1
        current_state = reallocate(current_state)

    print(f"The banks need to be reallocated {steps} times.")
    print(f"The loop has {steps - state_map[tuple(current_state)]} cycles.")


def reallocate(banks: list[int]) -> list[int]:
    blocks = max(banks)
    position = banks.index(blocks)
    banks[position] = 0

    while blocks > 0:
        position = (position + 1) % len(banks)
        banks[position] += 1
        blocks -= 1

    return banks


if __name__ == "__main__":
    main("input.txt")
