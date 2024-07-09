from common import *

import numpy as np
from typing import *

# concepts:
# cropping

# description:
# In the input you will see a single colored shape, around 4x6 in size, floating in a 12x12 grid of black.
# To make the output, crop the background out of the image - so the output grid has the same dimensions as the shape.

def main(input_grid):
    return crop(input_grid, background=Color.BLACK)

def generate_input():
    # create a roughly 12x12 input grid
    n = np.random.randint(10, 15)
    m = np.random.randint(10, 15)
    grid = np.full((n, m), Color.BLACK, dtype=int)

    # create a small random sprite with shape (2-7)x(2-7)
    w = np.random.randint(2, 8)
    h = np.random.randint(2, 8)
    sprite = random_sprite(w, h, color_palette=[np.random.choice(Color.NOT_BLACK)])

    # blit the spite onto a random location on the grid
    x, y = random_free_location_for_sprite(grid, sprite)
    blit_sprite(grid, sprite, x, y)
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
