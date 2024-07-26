from common import *

import numpy as np
from typing import *


# concepts:
# patterns, reflection, copying, translational symmetry

# description:
# In the input, you will see two mirrored patterns in the left and right halves of the grid.
# The grid will have a vertical axis of symmetry.
# To make the output, extract the left pattern of the input and repeat it horizontally to fill the entire output grid.

def main(input_grid):
    # Find the vertical axis of symmetry (middle of the grid)
    vertical_axis = input_grid.shape[1] // 2

    # Extract the left pattern
    left_pattern = input_grid[:, :vertical_axis]

    # Initialize the output grid with the same height as the input and double the width of the left pattern
    output_grid = np.zeros((input_grid.shape[0], 2 * vertical_axis), dtype=int)

    # Repeat the left pattern to fill the entire width of the output grid
    for i in range(2):
        blit_sprite(output_grid, left_pattern, y=0, x=i * vertical_axis)

    return output_grid

def generate_input():
    # Make a random sized grid with even width and odd height for symmetry purposes
    n = np.random.randint(4, 8)
    m = np.random.randint(3, 6) * 2  # Even width

    # Initialize the grid
    grid = np.zeros((n, m), dtype=int)

    # Select a color for the pattern
    color = np.random.choice(list(Color.NOT_BLACK))

    # Create a random pattern on the left half of the grid
    left_pattern = np.zeros((n, m // 2), dtype=int)
    for _ in range(np.random.randint(1, n * (m // 2) // 2 + 1)):
        x, y = np.random.randint(n), np.random.randint(m // 2)
        left_pattern[x, y] = color

    # Blit the left pattern onto the grid
    blit_sprite(grid, left_pattern, y=0, x=0)

    # Reflect the left pattern to the right half of the grid
    right_pattern = np.fliplr(left_pattern)
    blit_sprite(grid, right_pattern, y=0, x=m // 2)

    return grid