from common import *

import numpy as np
from typing import *

# concepts:
# horizontal bars, patterns, repeating pattern, symmetry detection

# description:
# In the input grid, each row may have a single color or follow an alternating/repeating pattern.
# For each row in the input, if that row has a single color, color that row in the output grey.
# If the row has a repeating or alternating pattern, color that row in the output green.
# If the row does not fit any of these categories, color it black in the output.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)

    for i in range(n):
        row = input_grid[i]
        unique_colors = np.unique(row[row != Color.BLACK])

        if len(unique_colors) == 1:
            # If the row is a single color, make it grey
            output_grid[i] = Color.GREY
        elif len(unique_colors) > 1 and has_repeating_pattern(row):
            # If the row has a repeating pattern, make it green
            output_grid[i] = Color.GREEN
        else:
            # Otherwise, it remains black
            output_grid[i] = Color.BLACK

    return output_grid

def has_repeating_pattern(row):
    """ Helper function to check for repeating or alternating pattern in the row """
    n = len(row)
    for k in range(1, n // 2 + 1):
        pattern = row[:k]
        if all((row[k * i : k * (i + 1)] == pattern).all() for i in range(n // k)):
            return True
        
    return False

def generate_input():
    n = np.random.randint(5, 15)
    m = np.random.randint(5, 15)
    grid = np.random.choice(list(Color.NOT_BLACK), size=(n, m))

    # Make some rows uniform in color
    for _ in range(np.random.randint(1, n // 2)):
        row = np.random.randint(n)
        color = np.random.choice(list(Color.NOT_BLACK))
        grid[row, :] = color

    # Make some rows follow a repeating pattern
    for _ in range(np.random.randint(1, n // 2)):
        row = np.random.randint(n)
        k = np.random.randint(2, m // 2 + 1)
        pattern = np.random.choice(list(Color.NOT_BLACK), size=k)
        grid[row, :] = np.tile(pattern, m // k + 1)[:m]

    return grid