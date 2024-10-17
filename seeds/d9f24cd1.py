from common import *

import numpy as np
from typing import *

# concepts:
# line drawing, obstacle recognition

# description:
# In the input you will see several red pixels on the bottom row of the grid, and some gray pixels scattered on the grid.
# To make the output grid, you should draw a red line from the bottom row to the top row. If it touch the gray pixel, 
# it should go right then up to avoid the gray pixel.

def main(input_grid):
    # The output grid is the same size as the input grid.
    output_grid = input_grid.copy()
    width, height = input_grid.shape

    # Iterate through the red pixels on the bottom row from left to right
    bottom_row = input_grid[:, -1]

    # Get the positions of the red pixels on the bottom row.
    for pos_x in np.argwhere(bottom_row == Color.RED):
        # Draw the red line from the bottom row to the top row.
        for pos_y in reversed(range(height)):
            if output_grid[pos_x, pos_y] != Color.GRAY:
                output_grid[pos_x, pos_y] = Color.RED
            else:
                # If the red line touch the gray pixel, it should go right then up to avoid the gray pixel.
                output_grid[pos_x + 1, pos_y + 1] = Color.RED
                pos_x += 1
                output_grid[pos_x, pos_y] = Color.RED
    return output_grid

def generate_input():
    # Generate the background grid with size of n x m.
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)

    # Generate the red pixels on the bottom row.
    # Get 3 random positions for the red pixels.
    available_postion = range(1, 9)
    red_location = random.sample(available_postion, 3)

    # Draw the red pixels on the bottom row.
    for pos_x in red_location:
        grid[pos_x, -1] = Color.RED
    
    # Get the region except the bottom row, left most column and right most column.
    # Randomly scatter the gray pixels on the grid.
    randomly_scatter_points(grid=grid[1:-1, 1:-1], color=Color.GRAY, density=0.1)
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)