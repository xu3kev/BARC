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
    n = np.random.randint(10, 14)
    m = np.random.randint(10, 14)
    grid = np.full((n, m), Color.BLACK, dtype=int)

    # create a small random object of a random color
    w = np.random.randint(2, 7)
    h = np.random.randint(2, 7)
    # TODO[Simon] replace with random_sprite function when working?
    object = np.full((w, h), np.random.choice(Color.NOT_BLACK), dtype=int)
    object[np.random.rand(w, h) < 0.25] = Color.BLACK
    if not is_contiguous(object):
        return generate_input()

    # blit the spite onto a random location on the grid
    x, y = random_free_location_for_object(grid, object)
    blit(grid, object, x, y)
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
