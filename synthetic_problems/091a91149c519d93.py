from common import *

import numpy as np
from typing import *

# concepts:
# diagonal mirroring, symmetry, color

# description:
# In the input, you will see a grid with some pixels colored randomly.
# The output should be the diagonal mirror image along the main diagonal (top-left to bottom-right)
# Any pixel at (i, j) should be moved to (j, i) in the output.

def main(input_grid):
    # dimensions of the input grid
    n, m = input_grid.shape

    # create an output grid with the same dimensions
    output_grid = np.zeros_like(input_grid)

    # iterate over the input grid to apply diagonal mirroring
    for i in range(n):
        for j in range(m):
            output_grid[j, i] = input_grid[i, j]

    return output_grid


def generate_input():
    # generate a grid of random dimensions between 5x5 and 10x10
    n = np.random.randint(5, 10)
    m = np.random.randint(5, 10)
    grid = np.zeros((n, m), dtype=int)
    
    # pick a random number of colors to use (at least 1, at most 5)
    num_colors = np.random.randint(1, 6)
    
    # pick `num_colors` distinct colors from the color palette
    colors_in_use = np.random.choice(list(Color.NOT_BLACK), num_colors, replace=False)
    
    # fill the grid with random colors from the colors_in_use
    for i in range(n):
        for j in range(m):
            grid[i, j] = np.random.choice(colors_in_use)
    
    return grid