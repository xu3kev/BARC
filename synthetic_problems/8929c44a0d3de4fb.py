from common import *
import numpy as np
from typing import *

# concepts:
# surrounding, patterns

# description:
# In the input, you will see a grid with black background and some randomly scattered grey pixels.
# For each of those grey pixels, map the grey pixel to a cross pattern.
# The cross pattern has a radius of 2 and the arms of the cross should extend horizontally and vertically.
# Thus, for each grey pixel, make a cross pattern (without exceeding the boundaries of the grid).

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    grey_pixels = np.argwhere(input_grid == Color.GREY)
    
    for x, y in grey_pixels:
        # Create horizontal and vertical arms of the cross pattern
        for d in range(-2, 3):
            if 0 <= x + d < input_grid.shape[0]:
                output_grid[x + d, y] = Color.BLUE
            if 0 <= y + d < input_grid.shape[1]:
                output_grid[x, y + d] = Color.BLUE
    
    # Ensure the center remains grey
    output_grid[input_grid == Color.GREY] = Color.GREY
    
    return output_grid


def generate_input():
    # create a grid with size between 9x9 and 15x15 filled with black (0)
    grid_size = np.random.randint(9, 16)
    grid = np.full((grid_size, grid_size), Color.BLACK)
    
    # sparsely populate it with grey pixels
    num_grey_pixels = np.random.randint(3, 7)
    for _ in range(num_grey_pixels):
        x = np.random.randint(0, grid_size)
        y = np.random.randint(0, grid_size)
        grid[x, y] = Color.GREY
    
    return grid