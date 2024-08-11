from common import *

import numpy as np
from typing import *
import random

# concepts:
# mirrored patterns, diagonal pixels, repetition, coloring

# description:
# In the input, we have a diagonal pattern of pixels in a certain color forming a stair-like structure.
# To produce the output, mirror this diagonal pattern across both vertical and horizontal midlines of the grid,
# producing four identical diagonal stairs.
# Additionally, color all the diagonal pixels adjacent to the original diagonal pattern teal.

def main(input_grid: np.ndarray) -> np.ndarray:
    n, m = input_grid.shape
    
    # Create output grid with mirrored patterns
    output_grid = np.copy(input_grid)
    
    # Mirror horizontally
    output_grid = np.concatenate((output_grid[:, ::-1], output_grid), axis=1)
    
    # Mirror vertically
    output_grid = np.concatenate((output_grid[::-1, :], output_grid), axis=0)
    
    # Create diagonal directions for coloring adjacent pixels teal
    diagonal_dx_dy = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    
    # Color diagonal pixels
    for y in range(output_grid.shape[1]):
        for x in range(output_grid.shape[0]):
            if output_grid[x, y] != Color.BLACK and output_grid[x, y] != Color.TEAL:
                for dx, dy in diagonal_dx_dy:
                    # Color diagonal pixel teal if it is black
                    if 0 <= x + dx < output_grid.shape[0] and 0 <= y + dy < output_grid.shape[1]:
                        if output_grid[x + dx, y + dy] == Color.BLACK:
                            output_grid[x + dx, y + dy] = Color.TEAL

    return output_grid


def generate_input() -> np.ndarray:
    # Generate a grid size
    n = m = np.random.randint(5, 10)
    
    # Initialize grid
    grid = np.zeros((n, m), dtype=int)
    
    # Select a color for the staircase
    color = random.choice(list(Color.NOT_BLACK))
    
    # Create a diagonal staircase pattern on the grid
    for i in range(min(n, m)):
        grid[i, i] = color
    
    return grid