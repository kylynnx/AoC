from map_factory import HappinessMapFactory
from seating_finder import MaximumHappinessSeatingFinder


def main(filename: str):
    happiness_map = HappinessMapFactory.create(filename)
    seating_finder = MaximumHappinessSeatingFinder()
    seating_finder.find_seating(happiness_map)
    print(seating_finder.optimal_happiness)

    HappinessMapFactory.add_host("kylynnx", happiness_map)
    seating_finder.reset()
    seating_finder.find_seating(happiness_map)
    print(seating_finder.optimal_happiness)


if __name__ == '__main__':
    main("../input.txt")
