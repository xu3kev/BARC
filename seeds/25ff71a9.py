from common import *

import numpy as np
from typing import *


# concepts:
# sliding objects

# description:
# In the input you will see a 3x3 grid with a contiguous shape on it.
# Slide the shape down by one pixel.

def main(input_grid):
    # find the connected component, which is a monochromatic object
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=True)
    obj = objects[0]

    # translate the object down by one pixel
    output_grid = translate(obj, 0, 1, background=Color.BLACK)

    return output_grid


def generate_input():
    # first create blank grid
    grid = np.zeros((3, 3), dtype=int)

    # while the grid is empty
    while grid.sum() == 0:

        # generate a random up to 3x3 sprite
        n = random.randint(1, 3)
        m = random.randint(1, 2)
        random_sprite_to_add = random_sprite(n, m, symmetry='not_symmetric', color_palette=[random.choice(Color.NOT_BLACK)])

        # choose a random location on the grid, ensuring the bottom row is empty
        x = random.randint(0, 2)
        y = random.randint(0, 2 - m)

        # place the sprite onto the grid
        blit_sprite(grid, random_sprite_to_add, x, y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)