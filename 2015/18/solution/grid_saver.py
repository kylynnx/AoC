from PIL import Image
from light_grid import LightGrid



class GridSaver:
    @staticmethod
    def grid_to_image(grid: LightGrid) -> Image:
        image = Image.new('L', (grid.dim_x, grid.dim_y), 'white')

        for current_y in range(grid.dim_y):
            for current_x in range(grid.dim_x):
                color = 255 * (1 - grid.get_cell(x=current_x, y=current_y))
                image.putpixel((current_x, current_y), color)

        return image

    @staticmethod
    def animate_grid(grid: LightGrid, steps: int, filename: str, stuck_corners: bool = False):
        frames = [GridSaver.grid_to_image(grid)]
        for _ in range(steps):
            grid.advance_single_step(stuck_corners)
            frames.append(GridSaver.grid_to_image(grid))

        frames[0].save(filename, format="GIF", save_all=True, append_images=frames[1:], duration=100, loop=0)
