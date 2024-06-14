from common import *

import numpy as np
from typing import *


# concepts:
# patterns, horizontal bars

# description:
# In the input you will see a colored pattern in a 3x3 grid.
# For each row of the input, if that row is a single color, color that row in the output grey. Otherwise, output black.

def main(input_grid):
    # get output grid ready
    output_grid = np.zeros((3, 3), dtype=int)

    # look at each row of the input grid
    for i, row in enumerate(input_grid.T):
        # check if each pixel in the row is the same color
        same_color = row[0] == row[1] == row[2]

        # if they are the same color, change the output row to grey
        if same_color:
            output_grid[0][i] = Color.GREY
            output_grid[1][i] = Color.GREY
            output_grid[2][i] = Color.GREY

    return output_grid

def generate_input():
    # create a 3x3 array of randomly chosen, non-black, colors
    grid = np.random.choise(Color.NOT_BLACK, size=(3, 3))

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)