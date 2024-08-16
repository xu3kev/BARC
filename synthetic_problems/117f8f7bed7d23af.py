from common import *

import numpy as np
from typing import *

# concepts:
# patterns, reflection, lines

# description:
# In the input, you will see a top row with a sequence of colored pixels.
# To make the output, first reflect this sequence of colored pixels to create a mirrored row at the bottom.
# Then, fill the rows between these two rows by alternating the original order and the inversed order of the colors in the top row.

def main(input_grid):
    # Get the top row of colors
    top_row_colors = input_grid[0, :]
    
    # Create the output grid with additional rows for the transformation
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)
    
    # Copy the top row to the output grid
    output_grid[0, :] = top_row_colors
    
    # Reflect the top row to the bottom row
    output_grid[-1, :] = top_row_colors[::-1]
    
    # Fill the rows in between by alternating the order and inverse order of the top row colors
    for i in range(1, n-1):
        if i % 2 == 1:
            output_grid[i, :] = top_row_colors
        else:
            output_grid[i, :] = top_row_colors[::-1]
    
    return output_grid

def generate_input():
    # Decide the length of the top row of colors
    length = np.random.randint(3, 6)
    
    # Create a random sequence of colors for the top row
    top_row_colors = np.random.choice(list(Color.NOT_BLACK), length, replace=False)
    
    # Create the input grid with one row of colors at the top
    grid = np.zeros((5, length), dtype=int)  # fixed height of 5 for simplicity; can be adjusted if needed
    grid[0, :] = top_row_colors
    
    return grid