from common import *

import numpy as np
from typing import *

# concepts:
# mirroring, patterns, connected components

# description:
# In the input, you will see a sprite on the left half of the grid centered on the vertical axis. 
# The goal is to mirror this sprite to the right half of the grid, creating a symmetrical pattern.

def main(input_grid):
    # Create a copy of the input grid for the output
    output_grid = np.copy(input_grid)

    # Find the vertical midpoint to determine the mirroring axis
    midpoint = input_grid.shape[1] // 2

    # Separate the left half of the grid where the sprite is located
    left_half = input_grid[:, :midpoint]

    # Mirror the left half to the right half
    right_half_mirrored = np.fliplr(left_half)

    # Place the mirrored right half onto the output grid
    output_grid[:, midpoint:] = right_half_mirrored

    return output_grid

def generate_input():
    # Create dimensions for the grid
    n, m = random.randint(5, 10), random.randint(10, 20)

    # Initialize an empty grid
    grid = np.full((n, m), Color.BLACK)

    # Randomly select a color for the sprite
    color = random.choice(list(Color.NOT_BLACK))

    # Generate a random sprite of [3, 4] x [3, 4] in the left half of the grid
    sprite = random_sprite([3, 4], [3, 4], symmetry="not_symmetric", color_palette=[color])

    # Place the sprite in the left half of the grid with some padding from the vertical axis
    x, y = random_free_location_for_sprite(grid[:, :m//2], sprite, background=Color.BLACK, padding=1, border_size=1)
    blit_sprite(grid, sprite, x, y)

    return grid