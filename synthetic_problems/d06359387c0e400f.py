from common import *

import numpy as np
from typing import *

# concepts: 
# objects, boundary tracing, color inversion
#
# description:
# In the input, you will have colored objects on a black background. Each object's boundary should be traced.
# If a boundary pixel is black, color it with the object's color, else invert the object's boundary color to black.
# The interior of the object remains unchanged.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # get the objects in the input grid
    objects = find_connected_components(input_grid)

    for obj in objects:
        color = obj[obj != Color.BLACK][0]  # Assuming monochromatic objects
        boundary = object_boundary(obj)

        for x, y in np.argwhere(boundary):
            if output_grid[x, y] == Color.BLACK:
                output_grid[x, y] = color
            else:
                output_grid[x, y] = Color.BLACK  # Inverting the boundary color

    return output_grid

def generate_input():
    # make a black 10x10 grid as the background
    n = m = 10
    grid = np.zeros((n, m), dtype=int)
    
    # create a few random colored sprites
    for _ in range(np.random.randint(3, 5)):  # Random number of objects
        sprite_color = np.random.choice(list(Color.NOT_BLACK))
        sprite = random_sprite(np.random.randint(2, 4), np.random.randint(2, 4), color_palette=[sprite_color], connectivity=4)
        
        try:
            x, y = random_free_location_for_object(grid, sprite, padding=1, padding_connectivity=4)
            blit(grid, sprite, x, y)
        except:
            pass  # If sprite doesn't fit, try the next 
    
    return grid