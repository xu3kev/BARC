from common import *

import numpy as np
from typing import *

# concepts:
# surrounding

# description:
# surround every gray pixel with blue pixels

def main(input_grid):
    output_grid = np.zeros_like(input_grid)

    for i in range(len(input_grid)):
        for j in range(len(input_grid[i])):
            if input_grid[i, j] == Color.GRAY:
                # if the current pixel is gray, then we need to surround it with blue
                output_grid[max(0, i-1):min(len(input_grid), i+2), max(0, j-1):min(len(input_grid[i]), j+2)] = Color.BLUE

    # but we need to keep the gray center: so copy over all the gray pixels
    output_grid[input_grid == Color.GRAY] = Color.GRAY
            
    return output_grid


# create a 9x9 grid of black (0) and then sparsely populate it with gray
def generate_input():
    # create a 9x9 grid of black (0)
    grid = np.zeros((9, 9), dtype=int)
    # sparsely populate it with gray
    for x in range(9):
        for y in range(9):
            if np.random.random() < 0.05:
                grid[x, y] = Color.GRAY
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)