from common import *

import numpy as np
from typing import *

# concepts:
# counting, incrementing, patterns, horizontal/vertical bars, topology

# description:
# In the input, you will see a 10x10 grid with a single colored pixel in the top-left corner.
# To make the output:
# 1. Start from the colored pixel and create horizontal and vertical bars of increasing length.
# 2. Each new bar should be one pixel longer than the previous bar in that direction.
# 3. Alternate between horizontal and vertical bars, starting with horizontal.
# 4. Continue this pattern until reaching the edge of the grid in either direction.
# 5. If a bar would exceed the grid boundary, stop the pattern in that direction.

def main(input_grid):
    # Get the color of the starting pixel
    color = input_grid[0, 0]
    
    # Initialize the output grid
    output_grid = np.zeros_like(input_grid)
    output_grid[0, 0] = color
    
    # Initialize variables
    x, y = 0, 0
    horizontal_length = 1
    vertical_length = 0
    
    while True:
        # Draw horizontal bar
        horizontal_length += 1
        if x + horizontal_length > input_grid.shape[1]:
            break
        output_grid[y, x:x+horizontal_length] = color
        x += horizontal_length - 1
        
        # Draw vertical bar
        vertical_length += 1
        if y + vertical_length > input_grid.shape[0]:
            break
        output_grid[y:y+vertical_length, x] = color
        y += vertical_length - 1
    
    return output_grid

def generate_input():
    # Create a 10x10 grid
    grid = np.zeros((10, 10), dtype=int)
    
    # Choose a random color (not black)
    color = np.random.choice(list(Color.NOT_BLACK))
    
    # Place the colored pixel in the top-left corner
    grid[0, 0] = color
    
    return grid