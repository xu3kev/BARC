from common import *

import numpy as np
from typing import *

# concepts:
# symmetric mirroring, shapes, deterministic transformation

# description:
# In the input you will see a grid containing colored shapes.
# The output grid should be the result of mirroring the input grid along a specified vertical axis.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Define the axis for the symmetric mirroring; for simplicity, we will use the vertical center (m//2)
    axis = m // 2
    
    for i in range(n):
        for j in range(m):
            # Mirroring across the vertical axis
            mirrored_j = 2 * axis - j if j != axis else j
            if 0 <= mirrored_j < m:
                output_grid[i, mirrored_j] = input_grid[i, j]

    return output_grid

def generate_input():
    # Create a random grid with colored shapes
    n, m = np.random.randint(5, 10, size=2)
    grid = np.zeros((n, m), dtype=int)

    # Populate the grid with random colored shapes
    num_shapes = np.random.randint(1, 4)
    for _ in range(num_shapes):
        shape = random_sprite(np.random.randint(2, 4), np.random.randint(2, 4), color_palette=None)
        x, y = random_free_location_for_object(grid, shape)
        blit(grid, shape, x, y, background=Color.BLACK)

    return grid

# Example usage to test the implementation