from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, patterns, color change, symmetry detection, objects

# description:
# In the input you will see a grid consisting of a blue sprite that is repeatedly translated horizontally, forming a row of the same sprite.
# To make the output, expand the input to have width 15, and continue to repeatedly translate the sprite horizontally. Change color of the translated parts to yellow.

def main(input_grid):
    # Plan:
    # 1. Find the repeated translation, which is a symmetry
    # 2. Extend the pattern by copying the sprite and its symmetric copies
    # 3. Change the color from blue to yellow for the added translations
    
    symmetries = detect_translational_symmetry(input_grid, ignore_colors=[])
    assert len(symmetries) > 0, "No translational symmetry found"

    # make the output (the width is now 15)
    output_grid = np.full((input_grid.shape[0], 15), Color.BLACK)
    
    # Copy all of the input pixels to the output, INCLUDING their symmetric copies (i.e. their orbit)
    for x, y in np.argwhere(input_grid != Color.BLACK):
        # Compute the orbit into the output grid
        for x2, y2 in orbit(output_grid, x, y, symmetries):
            output_grid[x2, y2] = input_grid[x, y]
    
    # Now we need to extend the pattern horizontally
    for x2, y2 in np.argwhere(output_grid[:input_grid.shape[0], :input_grid.shape[1]] != Color.BLACK):
        # Start from the end of the original pattern and translate it horizontally
        x, y = x2, y2 + input_grid.shape[1]
        while x < output_grid.shape[0] and y < output_grid.shape[1]:
            output_grid[x, y] = Color.YELLOW
            y += input_grid.shape[1]

    return output_grid

def generate_input():
    # grid is always 6x3
    grid = np.zeros((6, 3), dtype=int)

    # The input is always blue
    color = Color.BLUE

    # Creates a random smaller sprite, where the width (period) is chosen randomly
    width = random.randint(2, 4)
    sprite = random_sprite(6, width, symmetry="not_symmetric", color_palette=[color], density=0.4, connectivity=8)

    # place the smaller pattern, tiling it so that it is repeated horizontally
    # tile "infinitely" (x100)
    horizontally_repeated = np.tile(sprite, (100, 1))
    # crop to the size of the grid
    horizontally_repeated = horizontally_repeated[:grid.shape[0], :]
    # copy to the grid
    grid[:, :] = horizontally_repeated

    return grid