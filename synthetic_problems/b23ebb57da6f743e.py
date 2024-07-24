from common import *

import numpy as np
from typing import *

# concepts:
# colors as indicators, incrementing, scaling, positioning

# description:
# In the input, you will see a row partially filled with pixels of one color.
# To make the output:
# 1. Take the input row.
# 2. Copy it below the original row with twice as many colored pixels added to the sequence if there is space.
# 3. Repeat until there are half as many rows as there are columns.

def main(input_grid):
    # get the color of the row
    color = np.unique(input_grid[input_grid != Color.BLACK])[0]

    # copy the row from the input grid
    row = np.copy(input_grid)

    # make the output grid
    output_grid = np.copy(input_grid)

    # repeat the row on the output grid until there are half as many rows as there are columns
    num_columns = input_grid.shape[1]
    max_rows = num_columns // 2

    for _ in range(1, max_rows):
        # find the rightmost color pixel in the row and add twice as many pixels of the same color to the right if there is space
        rightmost_color_pixel = np.where(row[0] == color)[0][-1]
        if rightmost_color_pixel + 2 < num_columns:
            row[0, rightmost_color_pixel + 1:rightmost_color_pixel + 3] = color
        
        # add the row to the output grid
        output_grid = np.vstack((output_grid, row))

    return output_grid

def generate_input():
    # decide the number of columns (even), and ensure at least 2
    num_columns = np.random.randint(4, 15) * 2

    # decide the color to partially fill the row with
    color = np.random.choice(list(Color.NOT_BLACK))

    # make a row with the color partially filled from left to right
    row = np.zeros((1, num_columns), dtype=int)
    num_colored_pixels = np.random.randint(1, num_columns // 2 + 1)
    row[0, :num_colored_pixels] = color

    return row