from common import *

import numpy as np
from typing import *

# concepts: Reflection, Boundary Detection

# description:
# In the input grid, you will see a single colored shape occupying part of the grid.
# Your task is to reflect this shape across the vertical central axis of the grid and then mark only the boundary of the resulting shape with a different color.

def main(input_grid):
    # Determine grid size
    n, m = input_grid.shape

    # Reflect the shape across the vertical central axis
    reflected_grid = np.copy(input_grid)
    center_m = m // 2

    for x in range(n):
        for y in range(center_m):
            # Swap values with the opposite side of the vertical central axis
            reflected_grid[x, y] = input_grid[x, m - y - 1]
            reflected_grid[x, m - y - 1] = input_grid[x, y]

    # Detect boundary of the reflected shape
    boundary_grid = np.full_like(reflected_grid, Color.BLACK)
    shape_mask = np.zeros_like(reflected_grid)
    shape_mask[reflected_grid != Color.BLACK] = 1
    shape_boundary = object_boundary(shape_mask, background=0)

    # Mark boundary pixels with a different color (let's choose Color.RED)
    for x, y in np.argwhere(shape_boundary):
        boundary_grid[x, y] = Color.RED

    return boundary_grid

def generate_input():
    # Generate a 14x14 grid with a random shape
    n, m = 14, 14
    grid = np.full((n, m), Color.BLACK)
    
    # Create a random shape
    shape = random_sprite(n//2, m//2, density=0.4, symmetry="not_symmetric", color_palette=list(Color.NOT_BLACK))
    
    # Find random free location for the shape, ensuring it stays within bounds
    x, y = random_free_location_for_object(grid, shape)
    blit(grid, shape, x, y)
    
    return grid

# Example test code to show the problem and solution