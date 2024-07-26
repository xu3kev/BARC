from common import *

import numpy as np
from typing import *

def main(input_grid):
    n, m = input_grid.shape

    # Checking the type of symmetry from the border
    horizontal_symmetry = np.any(input_grid[:, 0] == Color.BLUE) or np.any(input_grid[:, -1] == Color.BLUE)
    vertical_symmetry = np.any(input_grid[0, :] == Color.YELLOW) or np.any(input_grid[-1, :] == Color.YELLOW)

    background_color = np.bincount(input_grid.flatten()).argmax()

    # Prepare the output grid
    output_grid = np.copy(input_grid)

    if horizontal_symmetry:
        for i in range(n // 2):
            for j in range(m):
                output_grid[n - 1 - i, j] = input_grid[i, j]

    if vertical_symmetry:
        for i in range(n):
            for j in range(m // 2):
                output_grid[i, m - 1 - j] = input_grid[i, j]
 
    return output_grid


def generate_input():
    grid_size = (15, 15)
    
    # Creating an empty grid
    grid = np.zeros(grid_size, dtype=int)

    # Generate random scattered colored pixels
    num_pixels = np.random.randint(10, 40)
    for _ in range(num_pixels):
        x, y = np.random.randint(0, 15, size=2)
        grid[x, y] = np.random.choice(list(Color.NOT_BLACK))

    # Decide on the type of symmetry
    horizontal_symmetry = np.random.choice([True, False])
    vertical_symmetry = np.random.choice([True, False])

    # Add indicators on the borders for the type of symmetry
    if horizontal_symmetry:
        for i in range(15):
            grid[i, 0] = Color.BLUE
            grid[i, -1] = Color.BLUE

    if vertical_symmetry:
        for j in range(15):
            grid[0, j] = Color.YELLOW
            grid[-1, j] = Color.YELLOW

    # Ensure the background color is black
    grid[grid == 0] = Color.BLACK

    return grid