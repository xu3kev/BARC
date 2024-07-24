from common import *

import numpy as np
from typing import *

# concepts:
# patterns, reflection, symmetry

# description:
# In the input, you will see an 8x8 grid with only the first two rows filled with
# random colored pixels, and the remaining rows are black.
# To make the output, copy the first two rows of the input.
# Then, for the remaining six rows, reflect the pattern of the two rows horizontally and repeat it.

def main(input_grid):
    # Create an empty output grid
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)

    # Copy the first two rows of the input grid to the output grid
    output_grid[:2, :] = input_grid[:2, :]

    # Reflect the first two rows horizontally
    reflected_pattern = input_grid[:2, ::-1]

    # Fill the remaining rows of the output grid with the reflected pattern
    for i in range(2, n):
        output_grid[i, :] = reflected_pattern[i % 2, :]

    return output_grid

def generate_input():
    # Create an empty 8x8 grid
    grid = np.zeros((8, 8), dtype=int)

    # Fill the first two rows randomly with colors except black
    for i in range(2):
        for j in range(8):
            grid[i, j] = np.random.choice(list(Color.NOT_BLACK))

    return grid