from common import *

import numpy as np
from typing import *
import random

# concepts:
# color, patterns, encoding

# description:
# In the input, you'll see a grid containing a sequence of rows with different colors. 
# Some rows are missing colors which create blank spaces on the grid.
# To make the output, propagate the colors from the filled rows to the adjoining missing colors using nearest neighbor rule.

def main(input_grid):
    output_grid = np.copy(input_grid)
    width, height = output_grid.shape

    # Find the color of the background
    background_color = np.argmax(np.bincount(output_grid.flatten()))

    for x in range(width):
        for y in range(height):
            if output_grid[x, y] == background_color:
                # Propagate color from the nearest non-background pixel
                # Check right
                if x + 1 < width and output_grid[x + 1, y] != background_color:
                    output_grid[x, y] = output_grid[x + 1, y]
                # Check left
                elif x - 1 >= 0 and output_grid[x - 1, y] != background_color:
                    output_grid[x, y] = output_grid[x - 1, y]
                # Check down
                elif y + 1 < height and output_grid[x, y + 1] != background_color:
                    output_grid[x, y] = output_grid[x, y + 1]
                # Check up
                elif y - 1 >= 0 and output_grid[x, y - 1] != background_color:
                    output_grid[x, y] = output_grid[x, y - 1]

    return output_grid


def generate_input():
    width, height = 10, 10
    input_grid = np.zeros((width, height), dtype=int)

    # randomly select non-background color rows with gaps
    num_rows = random.randint(2, 5)
    row_indices = random.sample(range(height), num_rows)
    colors = random.sample(list(Color.NOT_BLACK), num_rows)

    for i, row in enumerate(row_indices):
        color = colors[i]
        num_cells = random.randint(3, 6)
        cell_indices = random.sample(range(width), num_cells)
        for cell in cell_indices:
            input_grid[cell, row] = color

    return input_grid