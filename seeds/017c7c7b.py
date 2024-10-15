from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, symmetry detection

# description:
# In the input you will see a grid consisting of a blue sprite that is repeatedly translated vertically, forming a stack of the same sprite.
# To make the output, expand the input to have height 9, and continue to repeatedly translate the sprite vertically. Change color to red.
 
def main(input_grid):
    # Plan:
    # 1. Find the repeated translation, which is a symmetry
    # 2. Extend the pattern by copying the sprite and its symmetric copies
    # 3. Change the color from blue to red
    
    symmetries = detect_translational_symmetry(input_grid, ignore_colors=[], background=Color.BLACK)
    assert len(symmetries) > 0, "No translational symmetry found"

    # make the output (the height is now 9)
    output_grid = np.full((input_grid.shape[0], 9), Color.BLACK)
    
    # Copy all of the input pixels to the output, INCLUDING their symmetric copies (i.e. their orbit)
    for x, y in np.argwhere(input_grid != Color.BLACK):
        # Compute the orbit into the output grid
        for x2, y2 in orbit(output_grid, x, y, symmetries):
            output_grid[x2, y2] = input_grid[x, y]
    
    # Color change: blue -> red
    output_grid[output_grid == Color.BLUE] = Color.RED

    return output_grid


def generate_input():
    # grid is always 3x6
    grid = np.zeros((3, 6),dtype = int)

    # The input is always blue
    color = Color.BLUE

    # Creates a random smaller sprite, where the height (period) is chosen randomly
    height = random.randint(2, 7)
    sprite = random_sprite(3, height, symmetry="not_symmetric", color_palette=[color], density=0.4, connectivity=8)

    # place the smaller pattern, tiling it so that it is repeated vertically
    # tile "infinitely" (x100)
    vertically_repeated = np.tile(sprite, (1, 100))
    # crop to the size of the grid
    vertically_repeated = vertically_repeated[:, :grid.shape[1]]
    # copy to the grid
    grid[:,:] = vertically_repeated

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)