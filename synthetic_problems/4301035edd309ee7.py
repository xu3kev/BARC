from common import *

import numpy as np
from typing import *

# concepts:
# borders, lines, direction, symmetry

# description:
# In the input, you will see a rectangular grid with a single blue pixel.
# To make the output:
# 1. Draw a teal border around the entire grid with a thickness of one pixel.
# 2. From the blue pixel, draw red lines outward in all eight directions (horizontal, vertical, and diagonal) until they hit the teal border.
# 3. Color the four corner pixels of the grid yellow.
# The resulting pattern should be symmetric around the blue pixel.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.copy(input_grid)

    # Draw teal border
    draw_line(grid=output_grid, x=0, y=0, length=None, color=Color.TEAL, direction=(1,0))
    draw_line(grid=output_grid, x=n-1, y=0, length=None, color=Color.TEAL, direction=(0,1))
    draw_line(grid=output_grid, x=0, y=0, length=None, color=Color.TEAL, direction=(0,1))
    draw_line(grid=output_grid, x=0, y=m-1, length=None, color=Color.TEAL, direction=(1,0))

    # Find blue pixel
    blue_pixel = np.where(input_grid == Color.BLUE)
    x, y = blue_pixel[0][0], blue_pixel[1][0]

    # Draw red lines in all 8 directions
    directions = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]
    for dx, dy in directions:
        draw_line(grid=output_grid, x=x, y=y, length=None, color=Color.RED, direction=(dx,dy), stop_at_color=[Color.TEAL])

    # Color corners yellow
    output_grid[0, 0] = Color.YELLOW
    output_grid[0, m-1] = Color.YELLOW
    output_grid[n-1, 0] = Color.YELLOW
    output_grid[n-1, m-1] = Color.YELLOW

    return output_grid

def generate_input():
    # Make a rectangular black grid
    n = np.random.randint(7, 15)
    m = np.random.randint(7, 15)
    grid = np.zeros((n, m), dtype=int)

    # Place a single blue pixel randomly, but not on the border
    x = np.random.randint(1, n-1)
    y = np.random.randint(1, m-1)
    grid[x, y] = Color.BLUE

    return grid