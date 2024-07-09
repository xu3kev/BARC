from common import *
import numpy as np
from typing import *

# concepts:
# reflection, symmetry

# description:
# In the input you will see a grid with an arbitrary colored pattern.
# To make the output, reflect the pattern horizontally and vertically around the central point of the grid.

def main(input_grid):
    h, w = input_grid.shape
    output_grid = np.copy(input_grid)
    
    # Reflect horizontally
    for x in range(h):
        for y in range(w // 2):
            output_grid[x, y], output_grid[x, w - y - 1] = output_grid[x, w - y - 1], output_grid[x, y]
    
    # Reflect vertically
    for y in range(w):
        for x in range(h // 2):
            output_grid[x, y], output_grid[h - x - 1, y] = output_grid[h - x - 1, y], output_grid[x, y]
    
    return output_grid


def generate_input():
    # Create a grid with a random color pattern
    n = m = np.random.randint(5, 10)
    input_grid = random_sprite(n, m)

    return input_grid