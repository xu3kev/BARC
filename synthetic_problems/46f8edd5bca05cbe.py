from common import *
import numpy as np
from typing import *

# concepts:
# lines, patterns

# description:
# The input grid has a top row with a sequence of different colored pixels, and the row below is empty.
# To make the output, starting from the bottom row, draw diagonal lines (going from bottom left to top right) in the direction of each colored pixel in the bottom row, with the color of each diagonal line matching the color of the corresponding pixel in the bottom row.

def main(input_grid):
    # get a copy of the input grid to modify it
    output_grid = np.copy(input_grid)

    # get the colors from the top row
    colors = input_grid[0]

    # create diagonal lines from the bottom to the top row
    n_rows, n_cols = input_grid.shape
    for col in range(n_cols):
        for row in range(n_rows-2, -1, -1):
            if row + col < n_rows:
                output_grid[row+col, col] = colors[col]

    # retain the top row colors and the empty row below
    output_grid[0] = input_grid[0]
    output_grid[1] = input_grid[1]
    
    return output_grid

def generate_input():
    # decide how many colors to use
    n_cols = np.random.randint(5, 10)
    n_rows = n_cols + np.random.randint(5, 10)

    # make a grid
    grid = np.zeros((n_rows, n_cols), dtype=int)

    # select colors for the top row and place them
    colors = np.random.choice(list(Color.NOT_BLACK), n_cols, replace=False)
    grid[0] = colors

    # keep the second row empty
    grid[1] = Color.BLACK

    # the rest of the grid is initially empty and can be randomly colored for complexity
    for i in range(2, n_rows):
        for j in range(n_cols):
            if np.random.rand() < 0.1:
                grid[i, j] = np.random.choice(list(Color.NOT_BLACK))

    return grid