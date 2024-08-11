from common import *

import numpy as np
from typing import *

# concepts:
# borders, color guide

# description:
# In the input, you will see a rectangular grid with a single-colored border and a random pattern inside.
# To make the output, identify the border color, remove one pixel of the border (making it black), and fill the inner area with the previously extracted border color.

def main(input_grid):
    n, m = input_grid.shape

    # Identify the border color (assuming all four borders have the same color)
    border_color = input_grid[0, 1]  # Taking the top border's color (excluding corners)

    # Create a new grid with all cells filled with the border color
    output_grid = np.full((n, m), border_color, dtype=int)

    # Make the outer-most border black
    draw_line(grid=output_grid, x=0, y=0, length=None, color=Color.BLACK, direction=(1, 0))
    draw_line(grid=output_grid, x=n-1, y=0, length=None, color=Color.BLACK, direction=(0, 1))
    draw_line(grid=output_grid, x=0, y=0, length=None, color=Color.BLACK, direction=(0, 1))
    draw_line(grid=output_grid, x=0, y=m-1, length=None, color=Color.BLACK, direction=(1, 0))

    return output_grid


def generate_input():
    # Making a grid with a random size between 5 and 10
    n = np.random.randint(5, 11)
    m = np.random.randint(5, 11)
    grid = np.zeros((n, m), dtype=int)

    # Randomly select a border color
    border_color = np.random.choice(list(Color.NOT_BLACK))

    # Fill the border with the selected color
    draw_line(grid, x=0, y=0, length=None, color=border_color, direction=(1, 0))  # top border
    draw_line(grid, x=n-1, y=0, length=None, color=border_color, direction=(0, 1))  # bottom border
    draw_line(grid, x=0, y=0, length=None, color=border_color, direction=(0, 1))  # left border
    draw_line(grid, x=0, y=m-1, length=None, color=border_color, direction=(1, 0))  # right border

    # Fill the inner area with random colors except border_color
    for i in range(1, n-1):
        for j in range(1, m-1):
            grid[i, j] = np.random.choice([c for c in Color.NOT_BLACK if c != border_color])

    return grid