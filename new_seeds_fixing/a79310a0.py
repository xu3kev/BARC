from common import *

import numpy as np
from typing import *

# concepts:
# object moving, color changing

# description:
# In the input you will see a grid with a teal object.
# To make the output grid, you should move the teal object down by 1 pixel and change its color to red.

def main(input_grid):
    # Get the position of the single teal object.
    x, y, w, h = bounding_box(grid=input_grid, background=Color.BLACK)

    # Crop the teal object.
    teal_object = crop(grid=input_grid, background=Color.BLACK)

    # Get the output background grid.
    output_grid = np.zeros_like(input_grid)

    # Move the teal object down by 1 pixel and change its color to red.
    teal_object[teal_object == Color.TEAL] = Color.RED
    output_grid = blit_sprite(grid=output_grid, x=x, y=y + 1, sprite=teal_object, background=Color.BLACK)

    return output_grid

def generate_input():
    # Generate the background grid with size of n x n.
    grid_len = np.random.randint(4, 8)
    grid = np.zeros((grid_len, grid_len), dtype=int)

    # Randomly generate the teal object and place it on the grid.
    sprite_width, sprite_height = np.random.randint(1, grid_len - 1), np.random.randint(1, grid_len -1)
    sprite = random_sprite(n=sprite_width, m=sprite_height, color_palette=[Color.TEAL], density=0.5)
    x, y = random_free_location_for_sprite(grid=grid, sprite=sprite, border_size=1)
    grid = blit_sprite(x=x, y=y, grid=grid, sprite=sprite, background=Color.BLACK)
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
