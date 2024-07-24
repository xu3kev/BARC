from common import *

import numpy as np
from typing import *


# concepts:
# alignment, direction, topological deformation

# description:
# In the input, you will see a grid with several horizontally aligned segments of colored pixels with gaps between them.
# The goal is to close the gaps so that each segment forms a continuous line. The colored segments are aligned along the rows of the grid, and empty spaces
# between them need to be filled with the same color to complete the lines.


def main(input_grid):
    output_grid = np.copy(input_grid)
    
    n, m = input_grid.shape
    
    for row in range(n):
        # Keep track of the latest color we see as we scan each row
        current_color = Color.BLACK
        for col in range(m):
            if input_grid[row, col] != Color.BLACK:
                current_color = input_grid[row, col]
            elif current_color != Color.BLACK:
                # Fill the gaps
                output_grid[row, col] = current_color
    
    return output_grid


def generate_input():
    # Create a blank 10x10 grid
    grid = np.zeros((10, 10), dtype=int)
    
    for row in range(10):
        # Randomly choose a color that isn't black
        color = np.random.choice(list(Color.NOT_BLACK))
        
        # Place horizontal segments with random gaps in each row
        segments = np.random.randint(3, 6)
        for _ in range(segments):
            start_col = np.random.randint(0, 8)
            length = np.random.randint(1, 3)
            grid[row, start_col:start_col + length] = color
    
    return grid