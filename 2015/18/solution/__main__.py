from grid_saver import GridSaver
from light_grid import LightGrid


def main(filename: str, steps: int):
    grid = LightGrid(filename)
    grid.advance(steps=steps)
    print(grid.light_count)


def animate(filename: str, steps: int, image_name: str):
    grid = LightGrid(filename)
    GridSaver.animate_grid(grid=grid, steps=steps, filename=image_name)

if __name__ == "__main__":
    main("../input.txt", steps=100)
    animate("../input.txt", steps=3, image_name="../game_of_life.gif")
