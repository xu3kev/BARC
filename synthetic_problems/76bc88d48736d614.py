from common import *

import numpy as np
from typing import *


# concepts:
# symmetry, reflection, rotation, boundary wrapping

# description:
# The input grid consists of random colored pixels forming a pattern.
# Rotate the pattern 90 degrees clockwise and place the rotated pattern in one of the diagonals wrapping around the grid boundary.
# If wrapping around goes out of bounds of the grid, it continues from the opposite side, i.e., wrapping.
def main(input_grid):

    # The pattern should be rotated 90 degrees clockwise
    rotated_pattern = np.rot90(input_grid, k=-1)

    # Create an output grid initialized with the input grid
    output_grid = np.copy(input_grid)

    # Place the rotated pattern
    n, m = input_grid.shape
    for x in range(n):
        for y in range(m):
            new_x, new_y = (x + y) % n, (x - y) % m

            output_grid[new_x, new_y] = rotated_pattern[x, y]

    return output_grid


def generate_input():
    # Create a random grid of colored pixels
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.random.choice(list(Color.NOT_BLACK), size=(n, m), replace=True)

    return grid