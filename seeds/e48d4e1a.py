from common import *

import numpy as np
from typing import *

# concepts:
# counting

# description:
# In the input, you will see a 10x10 black grid. The grid has one row and one column colored solidly in a single color, forming a cross of that color across the grid. The grid also has H grey pixels in the rightmost column at the top of the grid.
# To create the output, convert the H grey pixels to be black. Then shift the "cross" H pixels to the left and H pixels down.

def main(input_grid):
    # 1. Calculate the shift amount: the number of grey pixels in the rightmost column
    H = np.sum(input_grid[-1, :] == Color.GREY)

    # 2. find the row and column of the cross, and its color.
    color = next(c for c in np.unique(input_grid) if c not in [Color.BLACK, Color.GREY])

    # find which column is fully colored with the color
    x = np.where(np.all(input_grid == color, axis=1))[0][0]
    # find which row is fully colored with the color
    y = np.where(np.all(input_grid == color, axis=0))[0][0]

    # shift the column and row down/left by H
    x -= H
    y += H

    # create the output grid by recreating the cross at the new location
    output_grid = np.full(input_grid.shape, Color.BLACK)
    output_grid[x, :] = color
    output_grid[:, y] = color

    return output_grid

def generate_input():
    # create a 10x10 black grid
    grid = np.full((10, 10), Color.BLACK)

    # choose a random column/row and color for the cross, and create it
    # the column/row should be at least 1 pixel away from the bottom left.
    x = np.random.randint(1, 10)
    y = np.random.randint(9)
    color = np.random.choice(Color.NOT_BLACK)
    grid[x, :] = color
    grid[:, y] = color

    # choose a random number of grey pixels to place in the rightmost column
    # it should be less than the column and row numbers
    H = np.random.randint(1, min(x, y))

    # color the rightmost column's top H pixels grey
    grid[-1, :H] = Color.GREY

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)

