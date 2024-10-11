from common import *

import numpy as np
from typing import *

# concepts:
# counting

# description:
# In the input, you will see a 10x10 black grid containing a few 2x2 squares. Each square contains 1-4 colors.
# To create the output, draw a green 2xL rectangle just below each 2x2 square, where L is the number of colors in the square.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = input_grid.copy()
    # find all connected components in the input grid
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=False)

    # for each object, draw a green rectangle below it of shape 2xL, where L is the number of colors in the square
    for obj in objects:
        obj_x, obj_y, obj_width, obj_height = bounding_box(obj, background=Color.BLACK)
        num_colors = len(np.unique(obj[obj != Color.BLACK]))
        green_rectangle = np.full((obj_width, num_colors), Color.GREEN)
        blit_sprite(output_grid, green_rectangle, obj_x, obj_y + obj_height, background=Color.BLACK)

    return output_grid


def generate_input():
    input_grid = np.full((10, 10), Color.BLACK)
    num_squares = np.random.randint(1, 5)
    for _ in range(num_squares):
        square = random_sprite(2, 2, density=1.0, color_palette=Color.NOT_BLACK)
        x, y = random_free_location_for_sprite(input_grid, square, padding=1)
        input_grid = blit_sprite(input_grid, square, x, y, background=Color.BLACK)

    return input_grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
