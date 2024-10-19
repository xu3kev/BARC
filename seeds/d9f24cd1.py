from common import *

import numpy as np
from typing import *

# concepts:
# line drawing, obstacle avoidance

# description:
# In the input you will see several red pixels on the bottom row of the grid, and some gray pixels scattered on the grid.
# To make the output grid, you should draw a red line upward from each red pixel, but avoiding the gray pixels.
# To avoid touching the gray pixels, go right to avoid them until you can go up again.

def main(input_grid):
    # The output grid is the same size as the input grid, and we are going to draw on top of the input, so we copy it
    output_grid = input_grid.copy()
    width, height = input_grid.shape

    # Get the positions of the red pixels on the bottom row
    for x, y in np.argwhere(input_grid == Color.RED):
        # Draw the red line upward, but move to the right to avoid touching gray pixels
        while 0 < y < height and 0 < x < width:
            if output_grid[x, y - 1] == Color.GRAY:
                # If the red line touch the gray pixel, it should go right then up to avoid the gray pixel.
                output_grid[x + 1, y] = Color.RED
                x += 1
            else:
                # Otherwise we go up
                output_grid[x, y - 1] = Color.RED
                y -= 1

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
    randomly_scatter_points(grid[1:-1, 1:-1], color=Color.GRAY, density=0.1)
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)