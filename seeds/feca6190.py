from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation, expanding

# description:
# In the input you will see a line with several color pixels.
# To make the output, you should expand the line to the top-right direction diagonally.
# 1. Create a square-shape output grid with the size of the number of non-black pixels in the input grid times the original grid width.
# 2. Place the input grid from bottom left to top right, each row is one pixel upper-right from the previous row.

def main(input_grid):
    # The output grid size is the number of non-black pixels in the input grid times the original grid width
    input_width = input_grid.shape[0]
    colors = np.unique(input_grid)
    colors = colors[colors != Color.BLACK]
    output_size = input_width * len(colors)
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Place the input grid from bottom left to top right, each row is one pixel upper-right from the previous row
    for i in range(output_size):
        blit_sprite(output_grid, input_grid, x=i, y=output_size - 1 - i)

    return output_grid

def generate_input():
    # Generate a line
    n = np.random.randint(3, 7)
    m = 1
    grid = np.zeros((n, m), dtype=int)

    # Randomly choose colors for each grid
    colors = np.random.choice(Color.NOT_BLACK, size=n, replace=False)
    for i in range(n):
        # Randomly assign a color to each pixel
        if np.random.rand() < 0.5:
            grid[i, 0] = colors[i]

    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
