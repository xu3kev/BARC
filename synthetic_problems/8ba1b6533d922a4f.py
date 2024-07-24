from common import *

import numpy as np
from typing import *

# concepts:
# patterns, occlusion, symmetry detection

# description:
# In the input you will see an object that is symmetric along the diagonal axis (top-left to bottom-right), except that some parts have been removed (covered in black pixels).
# To make the output, fill in the missing parts of the object to make it symmetric along the diagonal axis.

def main(input_grid):
    # Create a copy of the input grid to modify
    output_grid = input_grid.copy()

    # Get the dimensions of the grid
    n, m = input_grid.shape

    # Ensure the grid is square
    assert n == m, "The input grid must be square."

    # Iterate over each element above the diagonal
    for i in range(n):
        for j in range(i + 1, n):
            # If the cell is black and its symmetric counterpart is not, fill it with the color of its counterpart
            if input_grid[i, j] == Color.BLACK and input_grid[j, i] != Color.BLACK:
                output_grid[i, j] = input_grid[j, i]

            # If the counterpart is black and this cell is not, fill the counterpart with the color of this cell
            if input_grid[j, i] == Color.BLACK and input_grid[i, j] != Color.BLACK:
                output_grid[j, i] = input_grid[i, j]

            # Handling both being non-black. Should not happen in well-formed inputs as per problem description
            if input_grid[i, j] != Color.BLACK and input_grid[j, i] != Color.BLACK:
                assert input_grid[i, j] == input_grid[j, i], "The input grid is not properly symmetric."

    return output_grid


def generate_input():
    # Define grid size (between 7 and 10 for some variability)
    n = m = np.random.randint(7, 11)
    grid = np.zeros((n, m), dtype=int)

    # Create a random sprite that will be partially symmetric
    sprite_size = np.random.randint(3, n//2 + 1)
    sprite = random_sprite(sprite_size, sprite_size, density=0.5, symmetry='horizontal', color_palette=list(Color.NOT_BLACK))

    # Place the sprite symmetrically along the diagonal
    for i in range(sprite_size):
        for j in range(sprite_size):
            grid[i, j] = sprite[i, j]
            grid[j, i] = sprite[i, j]

    # Randomly remove some parts to create occlusion
    for i in range(n):
        for j in range(n):
            if np.random.random() < 0.2:
                grid[i, j] = Color.BLACK

    return grid