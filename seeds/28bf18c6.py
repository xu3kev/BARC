from common import *

import numpy as np
from typing import *


# concepts:
# patterns, repetition

# description:
# In the input you will see a nxm grid with some wxh pattern of non-black pixels.
# Return a 2wxh grid with the same pattern repeated twice.

def main(input_grid):
    # find the pattern in the input grid
    pattern = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)[0]

    # get the bounding box of the pattern and crop the input grid to only include the pattern
    _, _, width, height = bounding_box(pattern)
    pattern = crop(pattern)

    # prepare the output grid
    output_grid = np.full((2 * width, height), Color.BLACK)

    # and blit the pattern twice
    blit(output_grid, pattern, 0, 0)
    blit(output_grid, pattern, width, 0)

    return output_grid


def generate_input():
    # first create a randomly sized grid, somewhere between 10x10 and 20x20
    n = random.randint(10, 20)
    m = random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)

    # now we want to randomly choose a square pattern size between 2x2 and 5x5 and a color for the pattern, then generate the pattern
    w = random.randint(2, 5)
    h = w
    color = new_random_color()
    pattern = random_sprite(w, h, symmetry="not_symmetric", color_palette=[color], connectivity=8)

    # now we want to randomly place the pattern in the grid
    x, y = random_free_location_for_object(grid, pattern) # find the location
    blit(grid, pattern, x, y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)