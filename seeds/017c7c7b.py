from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, symmetry detection

# description:
# In the input you will see a grid consisting of a blue sprite that is repeatedly translated vertically, forming a stack of the same sprite.
# To make the output, expand the input to have height 9, and continue to repeatedly translate the sprite vertically. Change color to red.
 
def main(input_grid):
    input_height = input_grid.shape[1]

    # determine the period of the repeated vertical translation
    v_period = detect_vertical_periodicity(input_grid)
    
    # because the translation is vertical, this is the height of the sprite
    sprite = input_grid[:, :v_period]

    # check the sprite repeats until the end of the input (this is true assuming that we got the right period)
    repeatedly_translated = np.tile(sprite, (1, 100))[:, :input_height]
    assert np.all(np.equal(input_grid, repeatedly_translated))

    # make the output (the height is now 9)
    output_grid = np.zeros((input_grid.shape[0], 9), dtype=int)

    # Make the sprite red
    sprite[sprite == Color.BLUE] = Color.RED

    # Copy sprite to fill the entire grid
    # This means repeating it vertically
    # (note: we could use np.tile here, but we'll do it manually for clarity)
    for y in range(0, output_grid.shape[1], period):
        blit(output_grid, sprite, 0, y)

    return output_grid


def generate_input():
    # Create output grid, which is always 3x6
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
    # copy the sprite to the grid
    blit(grid, vertically_repeated, 0, 0)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)