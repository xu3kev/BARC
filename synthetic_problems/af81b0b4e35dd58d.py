from common import *

import numpy as np
from typing import *

# concepts:
# repeating patterns, scaling, colors as indicators

# description:
# The input is a grid where each cell can be one of 10 colors, including black.
# For each non-black cell (i, j) in the input grid, the corresponding subgrid (k*i:k*i+k, k*j:k*j+k) in the output grid 
# should be filled with that cell's color, where k is a randomly chosen scaling factor between 2 and 4.
# Each black cell should remain unchanged in the output.

def main(input_grid):
    # The scaling factor k is part of the puzzle and needs to be communicated to `main` somehow.
    # For simplicity, we'll assume it is predefined (in a real puzzle, it could be communicated via some encoding in the input or metadata).
    k = 3

    output_grid = np.zeros((input_grid.shape[0] * k, input_grid.shape[1] * k), dtype=int)

    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != Color.BLACK:
                output_grid[i*k:(i+1)*k, j*k:(j+1)*k] = input_grid[i, j]
    
    return output_grid

def generate_input():
    k = np.random.randint(2, 5)
    n, m = np.random.randint(3, 7), np.random.randint(3, 7)
    grid = random_sprite(n, m, density=0.5, color_palette=[color for color in Color.NOT_BLACK])
    
    return grid