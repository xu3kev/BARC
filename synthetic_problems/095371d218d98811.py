from common import *

import numpy as np
from typing import *

# concepts:
# borders, growing, counting

# description:
# In the input, you will see a rectangular grid with a single non-black pixel of any color near the center.
# To make the output, create a series of concentric borders around this pixel. Each border should be one pixel thick.
# The colors of the borders should alternate between red and blue, starting with red for the innermost border.
# The number of borders should equal the row number of the original colored pixel (counting from 0 at the top).

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)

    # Find the non-black pixel
    center = np.argwhere(input_grid != Color.BLACK)[0]
    x, y = center

    # Determine the number of borders to draw
    num_borders = x

    # Draw the borders
    for i in range(num_borders):
        color = Color.RED if i % 2 == 0 else Color.BLUE
        
        # Calculate the coordinates of the current border
        top = max(0, x - i - 1)
        bottom = min(n - 1, x + i + 1)
        left = max(0, y - i - 1)
        right = min(m - 1, y + i + 1)

        # Draw the border
        draw_line(output_grid, top, left, length=None, color=color, direction=(0, 1))
        draw_line(output_grid, top, right, length=None, color=color, direction=(1, 0))
        draw_line(output_grid, bottom, left, length=None, color=color, direction=(0, 1))
        draw_line(output_grid, top, left, length=None, color=color, direction=(1, 0))

    # Copy the original colored pixel
    output_grid[x, y] = input_grid[x, y]

    return output_grid

def generate_input():
    # Make a rectangular black grid
    n = np.random.randint(5, 15)
    m = np.random.randint(5, 15)
    grid = np.zeros((n, m), dtype=int)

    # Place a single colored pixel near the center
    center_x = n // 2 + np.random.randint(-2, 3)
    center_y = m // 2 + np.random.randint(-2, 3)
    
    # Ensure the pixel is not on the edge
    center_x = max(1, min(center_x, n-2))
    center_y = max(1, min(center_y, m-2))

    # Choose a random non-black color
    color = np.random.choice(list(Color.NOT_BLACK))
    grid[center_x, center_y] = color

    return grid