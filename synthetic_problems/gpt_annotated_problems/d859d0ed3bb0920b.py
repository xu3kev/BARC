from common import *

import numpy as np
from typing import *

# concepts:
# counting, incrementing, colors as indicators, symmetry detection

# description:
# In the input, you will see a single row with pixels of various colors.
# To make the output:
# 1. Take the input row as the first row of the output
# 2. For each subsequent row:
#    - If the previous row has an even number of non-black pixels, mirror it horizontally
#    - If the previous row has an odd number of non-black pixels, shift all non-black pixels one step to the right (wrapping around)
# 3. Repeat until the number of rows equals the number of non-black pixels in the original input

def main(input_grid):
    # Get the input row
    row = np.copy(input_grid[0])
    
    # Count non-black pixels in the input
    non_black_count = np.sum(row != Color.BLACK)
    
    # Initialize output grid with the input row
    output_grid = np.copy(input_grid)
    
    for _ in range(non_black_count - 1):  # -1 because we already have the first row
        prev_row = output_grid[-1]
        non_black_pixels = prev_row != Color.BLACK
        
        if np.sum(non_black_pixels) % 2 == 0:  # Even number of non-black pixels
            new_row = np.flip(prev_row)
        else:  # Odd number of non-black pixels
            new_row = np.copy(prev_row)
            color_indices = np.where(non_black_pixels)[0]
            new_indices = (color_indices + 1) % len(prev_row)
            new_row[new_indices] = prev_row[color_indices]
            new_row[color_indices] = Color.BLACK
        
        output_grid = np.vstack((output_grid, new_row))
    
    return output_grid

def generate_input():
    # Decide the length of the row
    length = np.random.randint(5, 10)
    
    # Create a row with random colors
    row = np.zeros((1, length), dtype=int)
    num_colored_pixels = np.random.randint(2, length + 1)
    color_indices = np.random.choice(length, num_colored_pixels, replace=False)
    colors = np.random.choice(list(Color.NOT_BLACK), num_colored_pixels)
    row[0, color_indices] = colors
    
    return row