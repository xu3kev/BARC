from common import *

import numpy as np
from typing import *


# concepts:
# symmetry detection, patterns, sprites

# description:
# In the input, you will get a grid where each row contains colored objects. If a row is symmetric around its center, it remains unchanged.
# If a row is asymmetric, transform it to be symmetric by reflecting its right side to its left.

def main(input_grid):
    n, m = input_grid.shape

    output_grid = input_grid.copy()

    for y in range(n):
        left = input_grid[y, :m//2]
        if m % 2 == 0:
            # even number of columns
            right = input_grid[y, m//2:]
        else:
            # odd number of columns, exclude middle element from the right part
            right = input_grid[y, m//2+1:]

        # Check if left and right are reflections of each other
        if not np.array_equal(left, right[::-1]):
            right_reflected = left[::-1]
            if m % 2 == 0:
                output_grid[y, m//2:] = right_reflected
            else:
                output_grid[y, m//2+1:] = right_reflected
                
    return output_grid

def generate_input():
    n = np.random.randint(5, 10)  # number of rows
    m = np.random.randint(5, 10)  # number of columns
    
    grid = np.empty((n, m), dtype=int)

    for y in range(n):
        row = np.random.choice(Color.NOT_BLACK, size=m)
        if np.random.rand() > 0.5:
            # Make the row symmetric
            row[:m//2] = row[m//2+m%2:][::-1]
        grid[y] = row

    return grid