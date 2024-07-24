from common import *

import numpy as np
from typing import *

def main(input_grid):
    # Get the grid dimensions
    n, m = input_grid.shape

    # Create the output grid by making a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Identify the vertical mirrored axis (we will assume it's the central vertical line)
    mirrored_axis = m // 2  # This works for both even and odd width grids
    
    for i in range(n):
        for j in range(mirrored_axis):
            # Mirrored index in same row
            mirrored_j = m - 1 - j
            
            # Fill in occluded pixels using mirrored symmetry
            if output_grid[i, j] == Color.BLACK:
                output_grid[i, j] = output_grid[i, mirrored_j]
            elif output_grid[i, mirrored_j] == Color.BLACK:
                output_grid[i, mirrored_j] = output_grid[i, j]

    return output_grid

def generate_input():
    # Randomly generate grid size
    n = np.random.randint(5, 10)
    m = np.random.randint(5, 10)
    
    # Create an empty grid with all black pixels
    grid = np.full((n, m), Color.BLACK)
    
    # Choose a random color palette
    color_palette = list(Color.NOT_BLACK)
    
    # Create a mirrored sprite and place it in the grid
    mid_point = m // 2
    for i in range(n):
        for j in range(mid_point):
            color = np.random.choice(color_palette)
            grid[i, j] = color
            grid[i, m - 1 - j] = color

    # Randomly occlude a few pixels
    num_occlusions = np.random.randint(1, (n * m) // 3)
    for _ in range(num_occlusions):
        x = np.random.randint(0, n)
        y = np.random.randint(0, m)
        grid[x, y] = Color.BLACK

    return grid