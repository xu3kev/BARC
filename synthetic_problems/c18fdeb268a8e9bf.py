from common import *

import numpy as np
from typing import *

# concepts:
# objects, creating borders, color guide

# description:
# In the input you will see a grid containing multiple objects of different colors, surrounded by black pixels.
# To make the output, add a one-pixel-wide gray border around each object.

def main(input_grid):
    # find all the objects in the input grid
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)

    # initialize the output grid with the input grid
    output_grid = input_grid.copy()

    for obj in objects:
        # find the interior and boundary of the object
        interior = object_interior(obj, background=Color.BLACK)
        boundary = object_boundary(obj, background=Color.BLACK)
        
        # create the gray border around the object, but only in the boundary
        for x, y in np.argwhere(boundary):
            output_grid[x, y] = Color.GREY

        for x, y in np.argwhere(interior):
            if output_grid[x+1, y] == Color.BLACK or output_grid[x-1, y] == Color.BLACK or output_grid[x, y+1] == Color.BLACK or output_grid[x, y-1] == Color.BLACK:
                output_grid[x, y] = Color.GREY

    return output_grid


def generate_input():
    grid_size = 15
    min_size = 3
    max_size = 5

    # Initialize an empty grid with background color
    grid = np.full((grid_size, grid_size), Color.BLACK)

    for _ in range(5):  # Generate 5 objects of random size
        # Generate a random object
        obj_size = np.random.randint(min_size, max_size + 1)
        obj = random_sprite(obj_size, obj_size, density=1, color_palette=Color.NOT_BLACK)

        # Find random position for the object
        x, y = random_free_location_for_object(grid, obj, border_size=1)
        
        # Place the object into the grid
        blit(grid, obj, x, y)

    return grid