from common import *

import numpy as np
from typing import *

# concepts:
# counting, incrementing, sliding objects

# description:
# In the input grid, you will see one row that contains colored pixels from left to right starting at index 0.
# This row is followed by black pixels. 
# To make the output: 
# 1. Copy this row
# 2. Slide the copied row one position to the right if there is space and the row remains within the boundaries of the grid.
# 3. Repeat until the row reaches the end of the grid.

def main(input_grid):
    # Copy the first row with colored pixels
    first_row = input_grid[0].copy()
    
    # Initialize the output grid
    output_grid = input_grid.copy()
    
    # Height of the grid
    num_rows = input_grid.shape[0]
    
    # Repeat sliding the row to the right until it reaches the end of the grid
    for i in range(1, num_rows):
        previous_row = output_grid[i - 1].copy()
        new_row = np.roll(previous_row, shift=1)
        new_row[0] = Color.BLACK
        output_grid[i] = new_row
        
    return output_grid

def generate_input():
    # Define the grid size
    rows = np.random.randint(5, 10)
    cols = np.random.randint(8, 15)
    
    # Initialize the grid with black pixels
    grid = np.full((rows, cols), Color.BLACK, dtype=int)
    
    # Choose a color for the filled pixels
    color = np.random.choice(list(Color.NOT_BLACK))
    
    # Define the length of the colored sequence
    length = np.random.randint(1, cols // 2 + 1)
    
    # Fill the first row with the chosen color for the given length starting from index 0
    grid[0, :length] = color
    
    return grid