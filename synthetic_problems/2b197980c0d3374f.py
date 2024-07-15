from common import *

import numpy as np
from typing import *

# concepts:
# patterns, lines, repetition, symmetry

# description:
# In the input, you will see a sequence of colored pixels forming a pattern on the first row of the grid.
# Below that row, there will be a grey line.
# To make the output, copy the first two rows of the input.
# Then, starting below the grey line, repeat the pattern of colors from the first row in a symmetrical manner.
# Fill the subsequent rows, alternating the pattern and its mirror image until you reach the bottom of the grid.

def main(input_grid):
    # Copy the first two rows to the output grid
    output_grid = np.copy(input_grid[:2, :])
    
    # Get the colors from the first row
    colors = input_grid[0, :]

    # Find the y-coordinate of the grey line
    grey_line_y = np.where(input_grid[1, :] == Color.GREY)[0][0]

    # Determine the height of the grid to know how many rows to fill below the grey line
    grid_height = input_grid.shape[0]
    fill_rows = grid_height - 2  # The number of rows we need to fill below the grey line
    
    # Fill rows below the grey line with the color pattern and its mirror images
    for i in range(fill_rows):
        if i % 2 == 0:
            # Direct copy of the color pattern
            output_grid = np.vstack((output_grid, colors))
        else:
            # Mirror image of the color pattern
            output_grid = np.vstack((output_grid, np.flip(colors)))
    
    return output_grid


def generate_input():
    # Set up grid dimensions with at least 5 rows and 5 columns
    rows = np.random.randint(5, 10)
    cols = np.random.randint(5, 10)
    grid = np.zeros((rows, cols), dtype=int)

    # Create random colors for the top row
    colors = np.random.choice(list(Color.NOT_BLACK), cols, replace=True)
    grid[0, :] = colors

    # Put a grey line below the top row
    grid[1, :] = Color.GREY

    return grid