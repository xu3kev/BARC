from common import *

import numpy as np
from typing import *

# concepts:
# growing, patterns, reflection symmetry, colors as indicators

# description:
# In the input you will see a colored pattern with a central differently-colored pixel. 
# Identify the color of this central pixel. Create horizontal and vertical reflections of the input grid that symmetrically surround the given input grid. 
# The output grid will be 3 times the size of the input grid in both dimensions (n*3 x m*3). 
# Place horizontal and vertical reflections of the input grid at all four corners in the output grid. 
# Keep the central differently-colored pixel in both reflections replaced by its color in all the copies formed.

def main(input_grid):
    # Get the dimensions of the input grid
    n, m = input_grid.shape

    # Initialize the output grid
    output_grid = np.zeros((n * 3, m * 3), dtype=int)
    
    # Copy the input grid to the center of the output grid
    output_grid[n:2*n, m:2*m] = input_grid

    # Find the different colored pixel in the center
    colors, counts = np.unique(input_grid, return_counts=True)
    center_color = colors[np.argmin(counts)]

    # Create horizontal and vertical reflections
    left_reflection = np.flip(input_grid, axis=1)
    right_reflection = np.flip(input_grid, axis=0)
    top_reflection = np.flip(input_grid, axis=0)
    bottom_reflection = np.flip(input_grid, axis=1)
    
    # Place the reflections in the output grid
    output_grid[0:n, 0:m] = left_reflection
    output_grid[2*n:3*n, 0:m] = right_reflection
    output_grid[0:n, 2*m:3*m] = top_reflection
    output_grid[2*n:3*n, 2*m:3*m] = bottom_reflection

    # Replace the differential pixel's new color across reflections
    output_grid[0:n, m:2*m][output_grid[0:n, m:2*m] == center_color] = center_color
    output_grid[2*n:3*n, m:2*m][output_grid[2*n:3*n, m:2*m] == center_color] = center_color
    output_grid[n:2*n, 0:m][output_grid[n:2*n, 0:m] == center_color] = center_color
    output_grid[n:2*n, 2*m:3*m][output_grid[n:2*n, 2*m:3*m] == center_color] = center_color
    
    return output_grid

def generate_input():
    # Create random dimensions for the input grid
    n, m = np.random.randint(3, 6, size=2)
    
    # Create random color for the pattern
    pattern_color = np.random.choice(list(Color.NOT_BLACK))
    
    # Create a random color for the central pixel different from the pattern color
    center_color = np.random.choice(list(Color.NOT_BLACK))
    while center_color == pattern_color:
        center_color = np.random.choice(list(Color.NOT_BLACK))

    # Create the input grid with pattern color
    input_grid = np.full((n, m), pattern_color)

    # Place the center color pixel randomly in the grid
    center_x, center_y = np.random.randint(n), np.random.randint(m)
    input_grid[center_x, center_y] = center_color
    
    return input_grid