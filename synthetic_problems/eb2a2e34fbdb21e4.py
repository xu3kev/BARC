from common import *

import numpy as np
from typing import *

# concepts:
# Reflection, Symmetry, Bounding Box

# description:
# In the input grid, identify the shape and find its bounding box.
# Reflect the shape horizontally and place the reflected shape to the right of the original one.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # find the connected components in the input grid
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True)
    
    # for simplicity, assume there's only one object in the grid
    obj = objects[0]

    # find the bounding box of the object
    x, y, w, h = bounding_box(obj)
    
    # get the sprite (cropped version of the obj)
    sprite = crop(obj)

    # reflect the sprite horizontally
    reflected_sprite = np.fliplr(sprite)

    # place the reflected sprite to the right of the original one
    blit(output_grid, reflected_sprite, x + w, y)

    return output_grid


def generate_input():
    # make a black grid as background
    n, m = np.random.randint(6, 10), np.random.randint(6, 10)
    grid = np.zeros((n, m), dtype=int)

    # choose a random color for the shape
    shape_color = np.random.choice(list(Color.NOT_BLACK))

    # make a random shape sprite
    sprite = random_sprite(n=np.random.randint(2, 4), m=np.random.randint(2, 4), color_palette=[shape_color], symmetry='not_symmetric')

    # place the sprite randomly in the grid
    x, y = random_free_location_for_object(grid, sprite)
    blit(grid, sprite, x, y)

    return grid