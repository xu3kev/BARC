from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation

# description:
# In the input you will see a grid with a single pixel on the bottom of the grid.
# To make the output, you should draw a geometric pattern starting outward from the pixel:
# step 1: draw vertical bars starting from the pixel and going to the right with a horizontal period of 2.
# step 2: put a grey pixel in between the vertical bars alternating between the top / bottom.

def main(input_grid):
    # Output grid is the same size as the input grid
    output_grid = np.zeros_like(input_grid)

    # Detect the pixel on the bottom of the grid
    pixel = find_connected_components(input_grid, monochromatic=True)[0]
    pixel_color = object_colors(pixel)[0]
    pixel_x, pixel_y = object_position(pixel)

    # Get the color of the pattern pixel by observation
    pattern_pixel_color = Color.GRAY
    
    # STEP 1: Draw vertical bar from bottom to top starting from the pixel and going to the right, horizontal period of 2
    horizontal_period = 2
    for x in range(pixel_x, output_grid.shape[0], horizontal_period):
        draw_line(output_grid, x=x, y=pixel_y, direction=(0, -1), color=pixel_color)
    
    # STEP 2: put a grey pixel in between the vertical bars alternating between the top / bottom.
    cur_y = -1 if pixel_y == 0 else 0
    for x in range(pixel_x + 1, output_grid.shape[0], horizontal_period):
        output_grid[x, cur_y] = pattern_pixel_color
        # alternate between top and bottom
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
