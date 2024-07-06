from common import *

import numpy as np
from typing import *

# concepts:
# reflection, symmetry

# description:
# In the input, you should see a series of colorful pixels.
# The task is to reflect these colorful pixels around the center horizontal axis of the grid.
# The reflected pixels should replace the black pixels on the other side of the axis.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    height, width = input_grid.shape
    mid_y = height // 2
    
    # Reflect pixels around the horizontal axis
    for x in range(width):
        for y in range(mid_y):
            if input_grid[y, x] != Color.BLACK:
                output_grid[height - y - 1, x] = input_grid[y, x]  # Reflecting the top part to bottom part

    return output_grid

def generate_input():
    height, width = np.random.randint(5, 8), np.random.randint(5, 8)  # Random grid size between 5x5 and 7x7
    input_grid = np.zeros((height, width), dtype=int)

    num_colored_pixels = np.random.randint(3, min(height * width, 10))  # Random number of colored pixels between 3 and 10
    for _ in range(num_colored_pixels):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height // 2)  # Pixels are placed in the top half only
        color = np.random.choice(list(Color.NOT_BLACK))
        input_grid[y, x] = color

    return input_grid