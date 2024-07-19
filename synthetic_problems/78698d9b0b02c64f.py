from common import *

import numpy as np
from typing import *

# concepts:
# color guide, patterns, pixel manipulation, symmetry

# description:
# In the input, you will see a symmetrical grid where half of the grid contains colored pixels in a random pattern.
# The other half of the grid is empty. 
# To make the output:
# 1. Identify the symmetrical axis.
# 2. Reflect the colored pixels from the filled half over to the empty half along the vertical or horizontal axis of symmetry, maintaining the symmetry.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    
    # Identify the symmetrical axis
    if np.all(input_grid[:, input_grid.shape[1] // 2] == Color.BLACK):
        # vertical symmetry
        for x in range(input_grid.shape[0]):
            for y in range(input_grid.shape[1] // 2):
                if input_grid[x, y] not in (Color.BLACK, Color.GREY):
                    output_grid[x, input_grid.shape[1] - 1 - y] = input_grid[x, y]

    elif np.all(input_grid[input_grid.shape[0] // 2, :] == Color.BLACK):
        # horizontal symmetry
        for x in range(input_grid.shape[0] // 2):
            for y in range(input_grid.shape[1]):
                if input_grid[x, y] not in (Color.BLACK, Color.GREY):
                    output_grid[input_grid.shape[0] - 1 - x, y] = input_grid[x, y]

    return output_grid

def generate_input() -> np.ndarray:
    # Create a symmetrical grid with a random pattern in half
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)

    # Decide if the symmetry should be vertical or horizontal
    vertical_symmetry = np.random.choice([True, False])

    # Generate a random pattern in half of the grid
    if vertical_symmetry:
        for x in range(n):
            for y in range(m // 2):
                if np.random.rand() > 0.5:
                    grid[x, y] = np.random.choice(list(Color.NOT_BLACK))
    else:
        for x in range(n // 2):
            for y in range(m):
                if np.random.rand() > 0.5:
                    grid[x, y] = np.random.choice(list(Color.NOT_BLACK))

    return grid