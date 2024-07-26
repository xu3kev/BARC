from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, reflection, patterns

# description:
# In the input you will see a colored pattern in the top-left quadrant of a grid.
# To make the output, create the entire grid by mirroring the top-left quadrant horizontally, vertically, and diagonally.

def main(input_grid):
    # Determine the size of the input grid and the quadrant
    n, m = input_grid.shape
    qn, qm = n // 2, m // 2  # assuming the input grid will always be of even dimensions

    # Extract the top-left quadrant
    top_left = input_grid[:qn, :qm]

    # Reflect the top-left quadrant horizontally
    top_right = np.fliplr(top_left)

    # Reflect the top-left quadrant vertically
    bottom_left = np.flipud(top_left)

    # Reflect the top-right quadrant vertically
    bottom_right = np.flipud(top_right)

    # Combine the quadrants to form the complete grid
    top_half = np.concatenate((top_left, top_right), axis=1)
    bottom_half = np.concatenate((bottom_left, bottom_right), axis=1)
    output_grid = np.concatenate((top_half, bottom_half), axis=0)

    return output_grid

def generate_input():
    # Create a randomly sized even-dimension grid, size from 6x6 to 10x10
    n = m = random.choice([6, 8, 10])
    grid = np.zeros((n, m), dtype=int)

    # Define the size of the top-left quadrant
    qn, qm = n // 2, m // 2

    # Create a random pattern in the top-left quadrant
    top_left_quadrant = random_sprite(qn, qm, density=1, symmetry="not_symmetric", color_palette=Color.NOT_BLACK)

    # Place this pattern on the grid
    blit_sprite(grid, top_left_quadrant, x=0, y=0, background=Color.BLACK)

    return grid