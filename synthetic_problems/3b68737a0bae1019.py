from common import *

import numpy as np
from typing import *

# concepts:
# patterns, copying, positioning

# description:
# In the input, you will see a pattern of colored pixels in the center of the grid.
# To make the output, replicate the input grid such that the pattern is moved to each corner of the grid, while maintaining the original pattern in the center.

def main(input_grid):
    # Find the connected components in the input grid
    objects = find_connected_components(input_grid, connectivity=8)

    # Assume there's only one central pattern in the input
    central_pattern = objects[0]

    # The bounding box of the central pattern
    x, y, w, h = bounding_box(central_pattern)

    # Extract the central sprite
    sprite = crop(central_pattern)

    # Create the output grid that is four times the size of the input grid
    output_grid = np.zeros((2 * input_grid.shape[0], 2 * input_grid.shape[1]), dtype=int)

    # Positions to place the patterns: top-left, top-right, bottom-left, bottom-right
    positions = [
        (0, 0),
        (0, output_grid.shape[1] - w),
        (output_grid.shape[0] - h, 0),
        (output_grid.shape[0] - h, output_grid.shape[1] - w)
    ]

    # Blit the sprite to the four corners of the output grid
    for (px, py) in positions:
        blit_sprite(output_grid, sprite, x=px, y=py, background=Color.BLACK)

    # Also keep the original central pattern at the center of the new grid
    central_x = output_grid.shape[0] // 2 - h // 2
    central_y = output_grid.shape[1] // 2 - w // 2
    blit_sprite(output_grid, sprite, x=central_x, y=central_y, background=Color.BLACK)

    return output_grid

def generate_input():
    # Make a random sized grid with black background
    n = np.random.randint(5, 8)
    m = np.random.randint(5, 8)
    grid = np.zeros((n, m), dtype=int)

    # Select a color for the patterns
    color = np.random.choice(list(Color.NOT_BLACK))

    # Select a size for the pattern so that it's in the center
    size = np.random.randint(2, min(n, m) // 2)

    # Generate a random pattern in the center of the grid
    start_x = (n - size) // 2
    start_y = (m - size) // 2

    for i in range(size):
        for j in range(size):
            if np.random.rand() > 0.5:
                grid[start_x + i, start_y + j] = color

    return grid