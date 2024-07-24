from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines, objects, topology

# description:
# In the input grid, there is one colored pixel on a black background.
# To make the output grid, create a criss-cross pattern with lines intersecting at the colored pixel. The lines should extend in 8 different directions (multiples of 45 degrees) around the center pixel, using the same color as the colored pixel.

def main(input_grid):
    # Make a copy of the input_grid to create the output grid
    output_grid = np.copy(input_grid)
    
    # Get the index of the colored pixel
    x, y, width, height = bounding_box(input_grid != Color.BLACK)
    
    # Get the color from the colored pixel
    color = input_grid[x, y]
    
    # Define directions for 45 degree increments
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    # Draw lines in each of the 8 directions
    for direction in directions:
        draw_line(output_grid, x, y, length=None, color=color, direction=direction)
    
    return output_grid

def generate_input():
    # Create a random-sized square black grid
    n = m = np.random.randint(5, 20)
    grid = np.zeros((n, m), dtype=int)
    
    # Place a randomly colored pixel at a random point on the grid
    color = random.choice(list(Color.NOT_BLACK))
    x, y = np.random.randint(0, n), np.random.randint(0, m)
    grid[x, y] = color
    
    return grid