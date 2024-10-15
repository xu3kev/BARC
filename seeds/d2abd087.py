from common import *

import numpy as np
from typing import *

# concepts:
# counting

# description:
# The input consists of several grey objects in a 10x10 grid.
# To create the output, change the color of all objects of area 6 to red, and all other objects to blue.

def main(input_grid):
    # extract objects
    objects = find_connected_components(input_grid, connectivity=4)

    # convert each object to the desired color
    for obj in objects:
        if np.sum(obj != Color.BLACK) == 6:
            obj[obj != Color.BLACK] = Color.RED
        else:
            obj[obj != Color.BLACK] = Color.BLUE

    # place new objects back into a grid
    output_grid = np.zeros_like(input_grid)
    for obj in objects:
        output_grid = blit_object(output_grid, obj, background=Color.BLACK)

    return output_grid


def generate_input():
    # create a 10x10 grid
    grid = np.full((10, 10), Color.BLACK)

    # generate objects and place into the grid until it is filled
    # we want some area six objects, and some non-area six objects.
    # to do so, first place a couple area six objects, then fill up the remaining space with random objects

    # place two area six objects
    for _ in range(2):
        while True:
            obj = random_sprite(list(range(1, 5)), list(range(1, 5)), color_palette=[Color.GREY])
            if np.sum(obj != Color.BLACK) == 6:
                break
        x, y = random_free_location_for_sprite(grid, obj, padding=1)
        grid = blit_sprite(grid, obj, x, y, background=Color.BLACK)

    # now fill up the remaining space with random objects.
    while True:
        obj = random_sprite(list(range(1, 5)), list(range(1, 5)), color_palette=[Color.GREY])

        # try to place the object. if we can't, we're done
        try:
            x, y = random_free_location_for_sprite(grid, obj, padding=1)
            grid = blit_sprite(grid, obj, x, y, background=Color.BLACK)
        except ValueError:
            break

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
