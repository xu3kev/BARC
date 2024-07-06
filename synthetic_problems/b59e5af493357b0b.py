from common import *

import numpy as np
import random

# concepts:
# pattern continuation, periodic patterns, grid transformation, pixel manipulation

# description:
# In the input grid, there will be a periodically repeating colored pattern with some parts missing. 
# The task is to complete the pattern in the output grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Get the dimensions of the input grid
    rows, cols = input_grid.shape

    # Find the pattern's size by detecting the smallest repeating unit
    max_pattern_size = min(rows, cols) // 2
    pattern_size = None

    for size in range(1, max_pattern_size + 1):
        is_repeating = True
        for r in range(size):
            for c in range(size):
                if input_grid[r, c] != input_grid[r + size, c] or \
                   input_grid[r, c] != input_grid[r, c + size]:
                    is_repeating = False
                    break
            if not is_repeating:
                break

        if is_repeating:
            pattern_size = size
            break

    assert pattern_size is not None, "No repeating pattern found"

    # Extract the pattern
    pattern = input_grid[:pattern_size, :pattern_size]

    output_grid = input_grid.copy()

    # Fill in the missing parts
    for r in range(0, rows, pattern_size):
        for c in range(0, cols, pattern_size):
            for i in range(pattern_size):
                for j in range(pattern_size):
                    if r + i < rows and c + j < cols and output_grid[r + i, c + j] == Color.BLACK:
                        output_grid[r + i, c + j] = pattern[i, j]

    return output_grid

def generate_input() -> np.ndarray:
    # Set the grid dimensions and pattern size
    rows, cols = 20, 20
    pattern_size = random.choice([2, 3, 4, 5])
    
    # Generate a random repeating pattern
    pattern = np.array(
        [[random.choice(list(Color.NOT_BLACK)) for _ in range(pattern_size)] for _ in range(pattern_size)]
    )

    # Create the grid by repeating the pattern
    grid = np.tile(pattern, (rows // pattern_size + 1, cols // pattern_size + 1))[:rows, :cols]

    # Randomly remove some parts of the pattern
    for _ in range(random.randint(5, 15)):
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        grid[r, c] = Color.BLACK

    return grid