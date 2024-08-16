from common import *

import numpy as np
from typing import *

# concepts:
# lines, color, counting

# description:
# In the input, you will see multiple vertical columns filled with either red, blue, or green pixels randomly placed on a black background.
# The task is to determine the number of pixels in each column.
# In the output, represent each count with a horizontal line of pixels (colored according to the original column's color) starting from the bottom of the grid.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)

    for col in range(m):
        column_colors = input_grid[:, col]
        unique, counts = np.unique(column_colors, return_counts=True)
        
        for color, count in zip(unique, counts):
            if color != Color.BLACK:
                # draw the horizontal line
                draw_line(output_grid, n-1, col, length=count, color=color, direction=(-1, 0))  # (-1, 0) is upward
    
    return output_grid


def generate_input():
    n = np.random.randint(10, 20)
    m = np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    num_columns = np.random.randint(3, m//2)
    columns_positions = np.random.choice(m, size=num_columns, replace=False)

    colors = [Color.RED, Color.BLUE, Color.GREEN]

    for col in columns_positions:
        color = np.random.choice(colors)
        num_pixels = np.random.randint(1, n)  # at least 1 pixel
        for _ in range(num_pixels):
            x = np.random.randint(0, n)
            grid[x, col] = color
    
    return grid