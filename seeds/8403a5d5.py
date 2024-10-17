from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation

# description:
# In the input you will see a grid with a single pixel on the bottom of the grid.
# To make the output, you should draw a pattern from the pixel.
# step 1: draw a line from the pixel to the right, each line has one pixel interval.
# step 2: put one pixel on the top / bottom interval alternatively.

def main(input_grid):
    # Output grid is the same size as the input grid
    output_grid = np.zeros_like(input_grid)

    # Detect the pixel on the bottom of the grid
    pixel = find_connected_components(input_grid, monochromatic=True)[0]
    pixel_color = object_colors(pixel)[0]
    x, y = object_position(pixel)

    # Get the color of the pattern pixel by observation
    pattern_pixel_color = Color.GRAY
    
    # STEP 1: Draw line from bottom to top from the pixel to right, each line has one pixel interval
    for i in range(x, output_grid.shape[0], 2):
        draw_line(output_grid, x=i, y=y, direction=(0, -1), color=pixel_color)
    
    # STEP 2: put one pixel on the top / bottom interval alternatively
    cur_y = 0
    for i in range(x + 1, output_grid.shape[0], 2):
        output_grid[i, cur_y] = pattern_pixel_color
        cur_y = 0 if cur_y == -1 else -1

    return output_grid

def generate_input():
    # Generate the background grid
    n, m = np.random.randint(10, 20, size=2)
    grid = np.zeros((n, m), dtype=int)

    # Randomly choose the color of the line
    pattern_pixel_color = Color.GRAY
    color = np.random.choice([color for color in Color.NOT_BLACK if color != pattern_pixel_color])

    # Randomly place the pixel on the bottom of the grid
    x = np.random.randint(0, n)
    grid[x, -1] = color

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
