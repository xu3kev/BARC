from common import *

import numpy as np
from typing import *

# concepts:
# lines, color, connectivity

# description:
# In the input, you will see a green pixel and a pink pixel.
# To make the output, draw a path of blue pixels that connects the green pixel to the pink pixel.
# The path should always move either horizontally or vertically, never diagonally.
# The path should take the shortest possible route between the two pixels.
# If there are multiple shortest paths, choose the one that goes right/left before going up/down.

def main(input_grid):
    # Copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # Find the green and pink pixels
    green_x, green_y = np.where(input_grid == Color.GREEN)
    pink_x, pink_y = np.where(input_grid == Color.PINK)

    # Extract coordinates
    start_x, start_y = green_x[0], green_y[0]
    end_x, end_y = pink_x[0], pink_y[0]

    # Draw horizontal line first
    x_direction = 1 if end_y > start_y else -1
    draw_line(output_grid, start_x, start_y, length=abs(end_y - start_y), color=Color.BLUE, direction=(0, x_direction))

    # Then draw vertical line
    y_direction = 1 if end_x > start_x else -1
    draw_line(output_grid, start_x, end_y, length=abs(end_x - start_x), color=Color.BLUE, direction=(y_direction, 0))

    return output_grid

def generate_input():
    # Make a black grid as the background
    n = np.random.randint(8, 20)
    m = np.random.randint(8, 20)
    grid = np.zeros((n, m), dtype=int)

    # Place green pixel
    green_x, green_y = np.random.randint(0, n), np.random.randint(0, m)
    grid[green_x, green_y] = Color.GREEN

    # Place pink pixel, ensuring it's not in the same row or column as the green pixel
    while True:
        pink_x, pink_y = np.random.randint(0, n), np.random.randint(0, m)
        if pink_x != green_x and pink_y != green_y:
            grid[pink_x, pink_y] = Color.PINK
            break

    return grid