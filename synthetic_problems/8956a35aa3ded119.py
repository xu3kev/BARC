from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, reflection

# description:
# In the input grid, you will see a pattern that has been flipped horizontally along the center of the grid. The left side of the grid contains the original pattern and the right side has the horizontally flipped version of the left side, but the right side is incomplete (i.e., some pixels are missing). 
# To create the output grid, fill in the missing pixels on the right side of the grid by copying the corresponding pixels from the left side of the grid.

def main(input_grid):
    # make output grid
    output_grid = np.copy(input_grid)
    
    # get the shape of the grid
    n, m = input_grid.shape
    
    # iterate over the left half of the grid
    for i in range(n):
        for j in range(m // 2):
            # check the corresponding position on the right half
            if output_grid[i, m - 1 - j] == Color.BLACK:
                # if the position is black, fill it with the color from the left half
                output_grid[i, m - 1 - j] = output_grid[i, j]
    
    return output_grid

def generate_input():
    # make a black grid
    n = np.random.randint(5, 10)
    m = np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)
    
    # generate a random pattern on the left half of the grid
    left_half_width = m // 2
    pattern = random_sprite(n, left_half_width, density=0.5, color_palette=Color.NOT_BLACK)
    for i in range(n):
        for j in range(left_half_width):
            grid[i, j] = pattern[i, j]

    # create the horizontally flipped version on the right half of the grid
    for i in range(n):
        for j in range(left_half_width):
            grid[i, m - 1 - j] = grid[i, j]

    # randomly remove some pixels from the right half
    for i in range(n):
        for j in range(left_half_width):
            if np.random.rand() < 0.3:
                grid[i, m - 1 - j] = Color.BLACK
    
    return grid