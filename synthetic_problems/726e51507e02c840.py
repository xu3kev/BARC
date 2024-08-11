from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, reflection, patterns

# description:
# In the input grid, you will see a pattern with a horizontal dividing line. 
# The bottom half is the reflection of the top half, but some pixels might be missing in the bottom half.
# To make the output, complete the reflection on the bottom half to be the true mirror image of the top half.

def main(input_grid: np.ndarray) -> np.ndarray:
    background_color = Color.BLACK

    n, m = input_grid.shape
    assert n % 2 == 0, "The input grid must have even number of rows for this puzzle to be symmetrical."

    top_half = input_grid[:n//2]
    bottom_half = input_grid[n//2:]

    # Reflect the top half to create the correct bottom half
    correct_bottom_half = np.flipud(top_half)

    # Fill in the missing parts in the bottom half to match the correct reflection
    filled_bottom_half = np.where(bottom_half == background_color, correct_bottom_half, bottom_half)

    # Create the output grid by combining top half and filled bottom half
    output_grid = np.vstack((top_half, filled_bottom_half))

    return output_grid

def generate_input() -> np.ndarray:
    n, m = np.random.randint(6, 10)*2, np.random.randint(6, 10)
    grid = np.zeros((n, m), dtype=int)

    # Populate the top half with a random pattern of three random colors
    random_colors = np.random.choice(list(Color.NOT_BLACK), 3, replace=False)
    top_half = random_sprite(n//2, m, density=0.5, color_palette=random_colors)

    # Create the correct bottom half by reflecting the top half
    correct_bottom_half = np.flipud(top_half)

    # Introduce randomness by missing some cells in the correct bottom half
    bottom_half = np.where(np.random.rand(n//2, m) > 0.1, correct_bottom_half, Color.BLACK)

    # Create the full input grid with the top and partially-filled bottom halves
    grid[:n//2, :] = top_half
    grid[n//2:, :] = bottom_half

    return grid