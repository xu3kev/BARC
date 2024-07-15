from common import *

import numpy as np
from typing import *

# concepts:
# borders, growing, pixel manipulation

# description:
# In the input, you will see a black grid with random colored pixels along the border.
# For the output, expand the border colored pixels inward by one pixel so that they stop just before they collide.

def main(input_grid: np.ndarray) -> np.ndarray:
    n, m = input_grid.shape
    output_grid = input_grid.copy()

    border_coords = [
        (x, 0) for x in range(n)
    ] + [
        (x, m-1) for x in range(n)
    ] + [
        (0, y) for y in range(m)
    ] + [
        (n-1, y) for y in range(m)
    ]

    # Create a temporary copy for modifications to avoid conflicts
    temp_grid = output_grid.copy()
    
    for x, y in border_coords:
        if output_grid[x, y] != Color.BLACK:
            color = output_grid[x, y]
            if x > 0 and output_grid[x - 1, y] == Color.BLACK:
                temp_grid[x - 1, y] = color
            if x < n - 1 and output_grid[x + 1, y] == Color.BLACK:
                temp_grid[x + 1, y] = color
            if y > 0 and output_grid[x, y - 1] == Color.BLACK:
                temp_grid[x, y - 1] = color
            if y < m - 1 and output_grid[x, y + 1] == Color.BLACK:
                temp_grid[x, y + 1] = color

    return temp_grid

def generate_input() -> np.ndarray:
    n = np.random.randint(5, 10)
    m = np.random.randint(5, 10)
    grid = np.zeros((n, m), dtype=int)

    border_coords = [
        (x, 0) for x in range(n)
    ] + [
        (x, m-1) for x in range(n)
    ] + [
        (0, y) for y in range(m)
    ] + [
        (n-1, y) for y in range(m)
    ]
    
    num_colors = np.random.randint(1, len(Color.NOT_BLACK) + 1)
    colors = random.sample(list(Color.NOT_BLACK), num_colors)
    
    for x, y in border_coords:
        if np.random.rand() > 0.6:
            grid[x, y] = random.choice(colors)

    return grid