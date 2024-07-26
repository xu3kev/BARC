from common import *

import numpy as np
from typing import *

# concepts:
# pattern detection, symmetry detection, growing

# description:
# You are given an input grid with a symmetric pattern in the top-left corner
# The task is to reflect this pattern across both axes to complete the entire grid
# Fill in the missing pixels to ensure symmetry and create a fully symmetric cross shape

def main(input_grid):
    # Make the output grid by copying the input grid
    output_grid = input_grid.copy()
    
    # Detect the pattern by finding its bounding box
    pattern_rows, pattern_cols = np.where(input_grid != Color.BLACK)
    min_row, max_row = pattern_rows.min(), pattern_rows.max()
    min_col, max_col = pattern_cols.min(), pattern_cols.max()
    
    # Get the pattern from the input grid
    pattern = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    # Reflect it vertically and horizontally to fill the entire grid
    grid_height, grid_width = input_grid.shape
    
    # Top-right reflection
    for i in range(max_row - min_row + 1):
        for j in range(max_col - min_col + 1):
            if grid_height > min_row + i and grid_width > (2 * max_col + 1 - min_col) - j - 1:
                output_grid[min_row + i, (2 * max_col + 1 - min_col) - j - 1] = pattern[i, j]

    # Bottom-left reflection
    for i in range(max_row - min_row + 1):
        for j in range(max_col - min_col + 1):
            if grid_height > (2 * max_row + 1 - min_row) - i - 1 and grid_width > min_col + j:
                output_grid[(2 * max_row + 1 - min_row) - i - 1, min_col + j] = pattern[i, j]
    
    # Bottom-right reflection
    for i in range(max_row - min_row + 1):
        for j in range(max_col - min_col + 1):
            if grid_height > (2 * max_row + 1 - min_row) - i - 1 and grid_width > (2 * max_col + 1 - min_col) - j - 1:
                output_grid[(2 * max_row + 1 - min_row) - i - 1, (2 * max_col + 1 - min_col) - j - 1] = pattern[i, j]
    
    return output_grid


def generate_input():
    # Create an empty grid with random size between 10 and 20
    grid_size = np.random.randint(10, 20)
    grid = np.zeros((grid_size, grid_size), dtype=int)
    
    # Define the size of the pattern (between 2x2 and 5x5)
    pattern_size = np.random.randint(2, 6)
    
    # Create the pattern
    pattern = random_sprite(pattern_size, pattern_size, density=0.5, color_palette=list(Color.NOT_BLACK))
    
    # Place the pattern in the top-left corner of the grid
    grid[0:pattern_size, 0:pattern_size] = pattern
    
    return grid