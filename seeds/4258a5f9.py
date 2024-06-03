from common import *

import numpy as np
from typing import *

black, blue, red, green, yellow, grey, pink, orange, teal, maroon = range(10)

# concepts:
# surrounding pixels

# description:
# surround every gray pixel with blue pixels

def main(input_grid):
    output_grid = np.zeros_like(input_grid)

    for i in range(len(input_grid)):
        for j in range(len(input_grid[i])):
            if input_grid[i][j] == grey:
                # if the current pixel is gray, then we need to surround it with blue
                output_grid[max(0, i-1):min(len(input_grid), i+2), max(0, j-1):min(len(input_grid[i]), j+2)] = blue

    # but we need to keep the gray center: so copy over all the gray pixels
    output_grid[input_grid == grey] = grey
            
    return output_grid


# create a 9x9 grid of black (0) and then sparsely populate it with gray
def generate_input():
    # create a 9x9 grid of black (0)
    grid = [[0 for i in range(9)] for j in range(9)]
    # sparsely populate it with gray
    for i in range(9):
        for j in range(9):
            if np.random.random() < 0.05:
                grid[i][j] = grey
    return np.array(grid)

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)