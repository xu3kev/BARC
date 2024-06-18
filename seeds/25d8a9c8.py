from common import *

import numpy as np
from typing import *


# concepts:
# patterns, horizontal bars

# description:
# In the input you will see a colored pattern in a 3x3 grid.
# For each row of the input, if that row is a single color, color that row in the output grey. Otherwise, output black.

def main(input_grid):
    # get input grid shape
    n, m = input_grid.shape

    # get output grid ready
    output_grid = np.zeros((n, m), dtype=int)

    # look at each row of the input grid
    for y in range(m):
        # check if each pixel in the row is the same color
        base_color = input_grid[0][y]
        all_same_color = True
        for color in input_grid[1:, y]:
            if color != base_color:
                all_same_color = False

        # if they are all the same color, change the output row to grey
        if all_same_color:
            for x in range(n):
                output_grid[x][y] = Color.GREY

    return output_grid

def generate_input():
    # create a 3x3 array of randomly chosen, non-black, colors
    grid = np.random.choice(Color.NOT_BLACK, size=(3, 3))

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)