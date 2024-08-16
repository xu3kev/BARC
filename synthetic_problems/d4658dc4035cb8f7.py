from common import *

import numpy as np
from typing import *

# concepts:
# objects, color, pixel manipulation, scaling

# description:
# In the input, there are several colored objects in a grid.
# To make the output, scale up each object by expanding each pixel in the object to a 2x2 block of pixels with the same color.

def main(input_grid):
    # get the objects in the input grid
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)

    # compute the new size of the output grid
    new_shape = (input_grid.shape[0] * 2, input_grid.shape[1] * 2)
    output_grid = np.zeros(new_shape, dtype=int)

    # scale up each object
    for obj in objects:
        color = np.unique(obj[obj != Color.BLACK])[0]
        for x, y in np.argwhere(obj != Color.BLACK):
            # expand each pixel to a 2x2 block
            output_grid[2*x:2*x+2, 2*y:2*y+2] = color

    return output_grid

def generate_input():
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    # generate a few random objects
    num_objects = np.random.randint(3, 6)
    for _ in range(num_objects):
        sprite_size = np.random.randint(2, 4)
        color = np.random.choice(list(Color.NOT_BLACK))
        sprite = random_sprite(sprite_size, sprite_size, density=0.5, color_palette=[color])
        try:
            x, y = random_free_location_for_object(grid, sprite, padding=1, padding_connectivity=4)
            blit(grid, sprite, x, y)
        except:
            pass

    return grid