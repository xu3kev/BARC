from common import *

import numpy as np
from typing import *

# concepts:
# colors, patterns, symmetry

# description:
# In the input, you will see a colored grid with multiple colors.
# To create the output grid, swap vertical mirrors of distinct colors: for any color in the left half of the grid, swap it with its mirror image in the right half of the grid.
# If the grid has an odd number of columns, the middle column's colors stay the same.

def main(input_grid):
    # Get the input grid dimensions
    n, m = input_grid.shape

    # Create a copy of the input grid to store the output
    output_grid = input_grid.copy()

    # Define the halfway point
    mid = m // 2

    # Iterate over the left half and right half of the grid, swapping mirrors
    for i in range(n):
        for j in range(mid):
            mirrored_j = m - 1 - j
            # Swap the colors
            output_grid[i, j], output_grid[i, mirrored_j] = input_grid[i, mirrored_j], input_grid[i, j]

    return output_grid

def generate_input():
    # Randomly decide the grid dimensions
    n = np.random.randint(3, 10)
    m = np.random.randint(3, 10)

    # Create a random grid with colors (excluding black)
    input_grid = np.random.choice(list(Color.NOT_BLACK), size=(n, m))

    return input_grid