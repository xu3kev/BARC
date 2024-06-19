from common import *

import numpy as np
from typing import *

# concepts:
# patterns, lines

# description:
# In the input, you will see a top row with a sequence of colored pixels, and right below it is a grey line.
# To make the output, copy the first two rows of the input. 
# Then, starting below the grey line, draw rows one color at a time in the order of the colors in the top row from left to right, with the color of each row matching the color of the corresponding pixel in the top row. 
# Repeat this pattern until you reach the bottom of the grid.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # get the colors from the top row
    colors = input_grid[:, 0]

    # get the number of colors
    num_colors = len(set(colors))

    # get the y-coordinate of the grey line
    grey_line = np.where(input_grid[0] == Color.GREY)[0][-1]

    # draw the rows below the grey line
    for i in range(input_grid.shape[1] - grey_line - 1):
        draw_line(output_grid, 0, grey_line + i + 1, length=None, color=colors[i % num_colors], direction=(1, 0))

    return output_grid





def generate_input():
    # decide how many colors to use
    num_colors = np.random.randint(2, 6)

    # select colors for the sequence
    colors = np.random.choice(list(Color.NOT_BLACK), num_colors, replace=False)

    # make a grid that will fit the colors along the top row, a grey line below it, and 2 times the number of colors rows below that
    n = num_colors
    m = 2 * num_colors + 2
    grid = np.zeros((n, m), dtype=int)

    # put the colors in the top row
    grid[:, 0] = colors

    # put a grey line below the top row
    grid[:, 1] = Color.GREY

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)