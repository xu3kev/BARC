from common import *

import numpy as np
from typing import *

# concepts:
# scaling

# description:
# In the input you will see a grid with different colors of pixels scattered on the grid
# To make the output grid, you should first only scale the pixels by 2 times,
# then scale in whole grid 2 times.

def main(input_grid):
    # Plan:
    # 1. Detect all the colored pixels
    # 2. Rescale each such sprite
    # 3. Blit the rescaled sprite onto the output grid, taking care to anchor it correctly
    # 4. Rescale the output grid (2x)

    # Detect all the colored pixels in the input grid
    pixel_objects = detect_objects(grid=input_grid, colors=Color.NOT_BLACK,
                            # These are single pixels, so they are 1x1
                            allowed_dimensions=[(1, 1)],
                            monochromatic=True, connectivity=4)

    # Initialize the output grid with the same size as the input grid
    output_grid = np.copy(input_grid)

    scale_factor = 2
    for obj in pixel_objects:
        # Get the position of each colored pixel, and crop it to produce a sprite
        x, y = object_position(obj, background=Color.BLACK, anchor="upper left")
        single_pixel_sprite = crop(obj, background=Color.BLACK)

        # Scale the sprite by `scale_factor` times
        scaled_sprite = scale_sprite(single_pixel_sprite, scale_factor)

        # The coordinate of the scaled pattern (anchored at the upper left)
        new_x, new_y = x - scale_factor + 1, y - scale_factor + 1

        # Put the scaled pattern on the output grid
        output_grid = blit_sprite(grid=output_grid, x=new_x, y=new_y, sprite=scaled_sprite, background=Color.BLACK)
    
    # Scale the whole grid by scale_factor times
    output_grid = scale_sprite(output_grid, scale_factor)

    return output_grid

def generate_input():
    # Generate the background grid with size of n x n.
    grid_size = 10
    grid = np.zeros((grid_size, grid_size), dtype=int)

    # randomly scatter the pixels on the grid with only every scaling_factor coordinates
    # Leave enough space for scaling
    density = 0.4
    scaling_factor = 2
    colors = Color.NOT_BLACK
    for x in range(1, grid_size, scaling_factor):
        for y in range(1, grid_size, scaling_factor):
            # Randomly scatter the pixels on the grid
            if np.random.rand() < density:
                grid[x, y] = np.random.choice(colors)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)