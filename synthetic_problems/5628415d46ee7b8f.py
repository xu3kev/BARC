from common import *

import numpy as np
from typing import *

# concepts:
# borders, patterns, horizontal bars

# description:
# In the input, you will see a grid with various horizontal or vertical stripes of different colors.
# For each stripe: If the stripe is horizontal, convert the stripe to all red.
# If the stripe is vertical, convert the stripe to all blue.
# If any repetitive pattern (group of same color) in the stripe is longer than half the length/height of the grid, also add a green border (thickness 1 pixel) around the grid.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.copy(input_grid)
    
    add_green_border = False
    
    for i in range(n):
        if np.all(output_grid[i, :] == output_grid[i, 0]):
            output_grid[i, :] = Color.RED  # Horizontal stripe
            if np.sum(output_grid[i, :] != Color.BLACK) > m // 2:
                add_green_border = True
    
    for j in range(m):
        if np.all(output_grid[:, j] == output_grid[0, j]):
            output_grid[:, j] = Color.BLUE  # Vertical stripe
            if np.sum(output_grid[:, j] != Color.BLACK) > n // 2:
                add_green_border = True

    if add_green_border:
        draw_line(grid=output_grid, x=0, y=0, length=n, color=Color.GREEN, direction=(1,0))
        draw_line(grid=output_grid, x=0, y=m-1, length=n, color=Color.GREEN, direction=(1,0))
        draw_line(grid=output_grid, x=0, y=0, length=m, color=Color.GREEN, direction=(0,1))
        draw_line(grid=output_grid, x=n-1, y=0, length=m, color=Color.GREEN, direction=(0,1))

    return output_grid


def generate_input():
    # Generate a random n x m grid
    n = np.random.randint(5, 10)
    m = np.random.randint(5, 10)
    grid = np.random.choice(list(Color.NOT_BLACK), size=(n, m))
    
    # Randomly decide rows or columns for stripes
    for i in range(n):
        if np.random.rand() < 0.3:
            grid[i, :] = np.random.choice(list(Color.NOT_BLACK))

    for j in range(m):
        if np.random.rand() < 0.3:
            grid[:, j] = np.random.choice(list(Color.NOT_BLACK))

    return grid