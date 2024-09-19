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
    # Detect all the colored pixels in the input grid
    pixels = detect_objects(grid=input_grid, colors=Color.NOT_BLACK, monochromatic=True, connectivity=4)

    # Initialize the output grid with the same size as the input grid
    output_grid = np.copy(input_grid)

    scale_factor = 2
    for pixel in pixels:
        # Get the position of each colored pixel and crop the pixel
        x, y, w, h = bounding_box(grid=pixel, background=Color.BLACK)
        single_pixel = crop(grid=pixel, background=Color.BLACK)
        # Scale the pattern by scale_factor times
        scaled_pattern = scale_pattern(pattern=single_pixel, scale_factor=scale_factor)

        # The coordinate of the scaled pattern is the top-left corner of the bounding box
        dx, dy = x - scale_factor + 1, y - scale_factor + 1

        # Put the scaled pattern on the output grid
        output_grid = blit_sprite(grid=output_grid, x=dx, y=dy, sprite=scaled_pattern, background=Color.BLACK)
    
    # Scale the whole grid by scale_factor times
    output_grid = scale_pattern(pattern=output_grid, scale_factor=scale_factor)

    return output_grid

def generate_input():
    # Generate the background grid with size of n x n.
    grid_size = 10
    grid = np.zeros((grid_size, grid_size), dtype=int)

    # randomly scatter the pixels on the grid with only every scaling_factor coordinates
    # Left enough space for scaling
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