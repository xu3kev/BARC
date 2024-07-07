from common import *

import numpy as np
from typing import *

# concepts:
# grid reflection, symmetry detection

# description:
# In the input grid, you will see various colored pixels.
# The transformation will reflect the grid about its center, both horizontally and vertically.
# The output grid will have these reflected pixels, maintaining symmetry about the center.

def main(input_grid):
    # Get the dimensions of the grid
    rows, cols = input_grid.shape
    
    # Create an output grid initialized with black pixels
    output_grid = np.zeros_like(input_grid)

    # Define the center of the grid
    center_row, center_col = rows // 2, cols // 2

    # Reflect the pixels about the center
    for i in range(rows):
        for j in range(cols):
            color = input_grid[i, j]
            if color != Color.BLACK:
                # Reflect across the center horizontally
                refl_i = 2 * center_row - i - 1
                # Reflect across the center vertically
                refl_j = 2 * center_col - j - 1
                # Place the color in the reflected positions
                output_grid[refl_i, j] = color  # Vertical reflection
                output_grid[i, refl_j] = color  # Horizontal reflection
                output_grid[refl_i, refl_j] = color  # Both reflections

    return output_grid


def generate_input():
    # Decide the dimensions of the grid
    rows, cols = 10, 10
    
    # Create an empty grid with black pixels
    grid = np.zeros((rows, cols), dtype=int)
    
    # Randomly place colored pixels on the grid, avoiding the center lines
    num_pixels = np.random.randint(5, 15)
    for _ in range(num_pixels):
        x = np.random.randint(0, rows)
        y = np.random.randint(0, cols)
        grid[x, y] = np.random.choice(list(Color.NOT_BLACK), 1)[0]

    return grid