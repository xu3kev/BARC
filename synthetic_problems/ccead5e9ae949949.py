from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, sprites

# description:
# In the input you will see several objects. One of these objects represents a sprite with 90-degree rotational symmetry. All the other objects represent non-symmetric sprites.
# The goal is to find the sprite with 90-degree rotational symmetry and return it.

def main(input_grid):
    # find the objects in the input grid
    objects = detect_objects(input_grid, background=Color.BLACK, monochromatic=False, connectivity=8)

    # crop out the sprites from the objects
    sprites = [crop(obj) for obj in objects]

    # find the 90-degree rotational symmetric sprite
    rotational_symmetric_sprite = None
    for sprite in sprites:
        # Check for 90-degree rotational symmetry
        if np.array_equal(sprite, np.rot90(sprite, 1)):
            rotational_symmetric_sprite = sprite
            break

    assert rotational_symmetric_sprite is not None, "No 90-degree rotational symmetric sprite found"
    return rotational_symmetric_sprite


def generate_input():
    # make a black 10x10 grid as background
    grid = np.zeros((10, 10), dtype=int)

    # choose the color of the sprite with 90-degree rotational symmetry
    color = np.random.choice(Color.NOT_BLACK)

    # choose the side length of the sprite
    side_length = np.random.randint(2, 5)

    # make the sprite with 90-degree rotational symmetry
    rotational_symmetric_sprite = random_sprite(side_length, side_length, symmetry='radial', color_palette=[color], connectivity=8)

    # place the rotational symmetric sprite randomly on the grid
    x, y = random_free_location_for_sprite(grid, rotational_symmetric_sprite, padding=1)
    blit_sprite(grid, rotational_symmetric_sprite, x=x, y=y)

    # add some non-symmetric sprites:
    for _ in range(np.random.randint(3, 6)):
        # choose the color of the sprite
        color = np.random.choice(Color.NOT_BLACK)

        # choose the side length of the sprite
        side_length = np.random.randint(2, 5)

        # make the non-symmetric sprite
        non_symmetric_sprite = random_sprite(side_length, side_length, symmetry="not_symmetric", color_palette=[color], connectivity=8)
        
        # place the non-symmetric sprite randomly on the grid if there is space
        try:
            x, y = random_free_location_for_sprite(grid, non_symmetric_sprite, padding=1)
            blit_sprite(grid, non_symmetric_sprite, x=x, y=y)
        except:
            pass

    return grid