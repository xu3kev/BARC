from common import *

import numpy as np
from typing import *

# concepts:
# mirror symmetry, drawing lines, filling

# description:
# In the input grid, you will see two vertical lines of different colors on the left side of the grid, 
# and two horizontal lines of different colors on the right side of the grid.
# For the output:
# 1. Mirror the colors from the left vertical lines to the right half of the grid.
# 2. Mirror the colors from the right horizontal lines to the bottom half of the grid.
# 3. Fill the regions formed by these lines with their respective colors.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Dimensions of the grid
    n, m = input_grid.shape
    
    # Find vertical lines
    left_lines = [(x, y) for x in range(n) for y in range(m//2) if input_grid[x, y] != Color.BLACK]
    for x, y in left_lines:
        color = input_grid[x, y]
        # Mirror to right half
        output_grid[x, m - y - 1] = color
    
    # Find horizontal lines
    right_lines = [(x, y) for x in range(n) for y in range(m//2, m) if input_grid[x, y] != Color.BLACK]
    for x, y in right_lines:
        color = input_grid[x, y]
        # Mirror to bottom half
        output_grid[n - x - 1, y] = color
    
    # Fill regions
    for x in range(n):
        for y in range(m):
            if output_grid[x, y] == Color.BLACK:
                if y < m//2:
                    for ly in range(m//2):
                        if output_grid[x, ly] != Color.BLACK:
                            fill_color = output_grid[x, ly]
                            output_grid[x, y] = fill_color
                            break
                else:
                    for ux in range(n):
                        if output_grid[ux, y] != Color.BLACK:
                            fill_color = output_grid[ux, y]
                            output_grid[x, y] = fill_color
                            break
    
    return output_grid


def generate_input():
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)
    
    # Two vertical lines on the left side with different colors
    left_colors = np.random.choice(list(Color.NOT_BLACK), 2, replace=False)
    for i, color in enumerate(left_colors):
        grid[:, i * 2] = color
    
    # Two horizontal lines on the right side with different colors
    right_colors = np.random.choice(list(Color.NOT_BLACK), 2, replace=False)
    for i, color in enumerate(right_colors):
        grid[i * 2, m//2:] = color

    return grid