from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, occlusion, diagonal lines

# description:
# In the input, you will see a single pixel of a color (not black) and a black rectangle that occludes part of the grid.
# To make the output:
# 1. Draw a horizontal line of the same color as the single pixel, intersecting at the pixel's position
# 2. Draw a vertical line of the same color as the single pixel, intersecting at the pixel's position
# 3. The lines should extend until the edges of the grid

def main(input_grid):
    output_grid = np.copy(input_grid)

    # Get the indices of the colored pixel
    colored_pixel_idx = np.argwhere(input_grid != Color.BLACK)[0]
    color = input_grid[colored_pixel_idx[0], colored_pixel_idx[1]]

    # Draw the horizontal line
    draw_line(output_grid, colored_pixel_idx[0], colored_pixel_idx[1], length=None, color=color, direction=(0, 1)) # Right
    draw_line(output_grid, colored_pixel_idx[0], colored_pixel_idx[1], length=None, color=color, direction=(0, -1)) # Left

    # Draw the vertical line
    draw_line(output_grid, colored_pixel_idx[0], colored_pixel_idx[1], length=None, color=color, direction=(1, 0)) # Down
    draw_line(output_grid, colored_pixel_idx[0], colored_pixel_idx[1], length=None, color=color, direction=(-1, 0)) # Up
    
    return output_grid

def generate_input():
    # Generate a black grid
    n, m = np.random.randint(8, 15), np.random.randint(8, 15)
    grid = np.zeros((n, m), dtype=int)

    # Place a randomly colored pixel at a random position on the grid
    color = random.choice(list(Color.NOT_BLACK))
    x, y = np.random.randint(1, n-1), np.random.randint(1, m-1)
    grid[x, y] = color

    # Place a black rectangle on the grid to occlude some of the lines
    rect_height = np.random.randint(2, 5)
    rect_width = np.random.randint(2, 5)
    rect_x = np.random.randint(0, n-rect_height)
    rect_y = np.random.randint(0, m-rect_width)
    grid[rect_x:rect_x+rect_height, rect_y:rect_y+rect_width] = Color.BLACK

    return grid