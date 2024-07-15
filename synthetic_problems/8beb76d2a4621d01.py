from common import *

import numpy as np
from typing import *

# concepts:
# patterns, lines, repetition, growing

# description:
# In the input, you will see a left column with a sequence of colored pixels, and right next to it is a grey line.
# To make the output, copy the first two columns of the input. 
# Then, starting to the right of the grey line, draw columns of increasing width.
# The color of each column matches the color of the corresponding pixel in the left column, from top to bottom.
# The width of each column increases by 1 pixel each time, starting from 1.
# Repeat this pattern until you reach the right edge of the grid.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # get the colors from the left column
    colors = input_grid[0, :]

    # get the number of colors
    num_colors = len(set(colors))

    # get the x-coordinate of the grey line
    grey_line = np.where(input_grid[:, 0] == Color.GREY)[0][-1]

    # draw the columns to the right of the grey line
    current_x = grey_line + 1
    column_width = 1
    while current_x < input_grid.shape[1]:
        for i in range(num_colors):
            if current_x + column_width > input_grid.shape[1]:
                break
            for j in range(column_width):
                draw_line(output_grid, current_x + j, 0, length=None, color=colors[i], direction=(0, 1))
            current_x += column_width
        column_width += 1

    return output_grid

def generate_input():
    # decide how many colors to use
    num_colors = np.random.randint(2, 6)

    # select colors for the sequence
    colors = np.random.choice(list(Color.NOT_BLACK), num_colors, replace=False)

    # make a grid that will fit the colors along the left column, a grey line next to it, and enough space for the growing columns
    n = 20  # Fixed height
    m = num_colors  # Width depends on the number of colors
    grid = np.zeros((n, m), dtype=int)

    # put the colors in the left column
    grid[0, :] = colors

    # put a grey line next to the left column
    grid[:, 1] = Color.GREY

    return grid