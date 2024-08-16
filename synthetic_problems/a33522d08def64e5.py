from common import *

import numpy as np
from typing import *

# concepts:
# reflection, color matching, mirroring, patterns

# description:
# In this puzzle, you will see a grid with various colored pixels forming patterns or shapes.
# Your task is to create a horizontally mirrored image of the original grid.

def main(input_grid):
    # Create an output grid of the same size as input
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the input grid
    n, m = input_grid.shape
    
    # Loop through each pixel and reflect it horizontally
    for x in range(n):
        for y in range(m):
            output_grid[x, m-y-1] = input_grid[x, y]
    
    return output_grid

def generate_input():
    n, m = np.random.randint(10, 20, size=2)
    grid = np.zeros((n, m), dtype=int)
    
    # Randomly decide the number of shapes/patterns
    num_shapes = np.random.randint(5, 10)
    
    for _ in range(num_shapes):
        # Randomly choose shape parameters
        shape_height = np.random.randint(1, n//2)
        shape_width = np.random.randint(1, m//2)
        start_x = np.random.randint(0, n - shape_height)
        start_y = np.random.randint(0, m - shape_width)
        shape_color = np.random.choice(list(Color.NOT_BLACK))
        
        # Create the shape within the grid
        grid[start_x:start_x+shape_height, start_y:start_y+shape_width] = shape_color
    
    return grid