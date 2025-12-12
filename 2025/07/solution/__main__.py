from manifold import Manifold


def main(filename: str):
    manifold = Manifold(filename)
    print(f"The beam is being split {manifold.active_beam_splitters} times.")
    print(f"In total there are {manifold.timelines} timelines in this manifold.")


if __name__ == "__main__":
    main("../test.txt")
    main("../input.txt")
