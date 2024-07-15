from common import *
import numpy as np
from typing import *

# concepts:
# object reflection, object boundary detection

# description:
# In the input you will see a non-black object of arbitrary size and shape.
# Reflect the object along its left boundary, and the reflected part should replace the black pixels to the left.

def main(input_grid):
    # Find the bounding box of the non-black pixels
    x, y, width, height = bounding_box(input_grid)
    
    # Extract the object based on the bounding box
    object_grid = input_grid[x:x + width, y:y + height]
    
    # Calculate the boundary of the object
    boundary = object_boundary(object_grid, background=Color.BLACK)
    
    # Reflect the object along the y-axis
    reflected_object = np.flip(object_grid, axis=1)

    # Create output grid with input dimensions
    output_grid = np.full_like(input_grid, Color.BLACK)

    # Place reflected object onto output grid, aligning it to touch the left boundary of the original object
    blit(output_grid, reflected_object, x, y - width if y - width >= 0 else 0, background=Color.BLACK)
    
    # Place original object onto output grid
    blit(output_grid, object_grid, x, y, background=Color.BLACK)

    return output_grid

def generate_input():
    # Make a black grid first as background
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    # Create a random non-black colored sprite object
    sprite = random_sprite(random.randint(3, 4), random.randint(3, 4), color_palette=Color.NOT_BLACK)
    
    # Place the sprite at a random location ensuring itâs not too close to left boundary
    x, y = random_free_location_for_object(grid, sprite, background=Color.BLACK, padding=2)
    blit(grid, sprite, x, y, background=Color.BLACK)
    
    return grid