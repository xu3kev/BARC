from common import *

import numpy as np
from typing import *

def main(input_grid):
    # Make output grid
    output_grid = np.copy(input_grid)

    # Get the index of the yellow pixel
    yellow = np.where(input_grid == Color.YELLOW)
    yellow_x, yellow_y = yellow[0][0], yellow[1][0]

    # Get the index of the pink pixel
    pink = np.where(input_grid == Color.PINK)
    pink_x, pink_y = pink[0][0], pink[1][0]

    # Draw yellow vertical and horizontal lines across the yellow pixel's coordinates
    output_grid[yellow_x, :] = Color.YELLOW
    output_grid[:, yellow_y] = Color.YELLOW

    # Draw pink diagonal line from top-left to bottom-right corner
    n = input_grid.shape[0]
    for i in range(n):
        output_grid[i, i] = Color.PINK

    return output_grid

def generate_input():
    # Make a NxN black grid for the background
    n = np.random.randint(7, 10)
    grid = np.zeros((n, n), dtype=int)

    # Place a yellow pixel at a random point on the grid
    yellow_x, yellow_y = np.random.randint(0, n, size=2)
    grid[yellow_x, yellow_y] = Color.YELLOW

    # Place a pink pixel at a random point on the grid but not in the same row or column as the yellow pixel
    pink_x, pink_y = np.random.randint(0, n, size=2)
    while pink_x == yellow_x or pink_y == yellow_y:
        pink_x, pink_y = np.random.randint(0, n, size=2)
    grid[pink_x, pink_y] = Color.PINK

    return grid