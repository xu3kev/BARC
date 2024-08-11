from common import *

import numpy as np
from typing import *

# concepts:
# topological, objects, color, patterns

# description:
# In the input grid, you will see multiple ring-shaped objects made up of different colors. 
# The output should fill the interior of each ring with the same color as the ring, making them solid colored circles.

def main(input_grid):
    output_grid = np.copy(input_grid)

    # find connected components in the grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=True)

    for obj in objects:
        # extract the bounding box of the object
        x, y, width, height = bounding_box(obj)
        
        # crop the object to get the sprite
        sprite = crop(obj)

        # find the color of the ring
        ring_color = np.unique(sprite[sprite != Color.BLACK])[0]

        # find the interior of the ring
        interior_mask = object_interior(sprite, background=Color.BLACK)

        # fill the interior with the ring color
        sprite[interior_mask] = ring_color

        # blit the filled sprite back to the output grid
        blit_sprite(output_grid, sprite, x, y, background=Color.BLACK)

    return output_grid

def generate_input():
    n = np.random.randint(10, 28)
    m = np.random.randint(10, 28)
    input_grid = np.full((n, m), Color.BLACK)

    # Generate random ring shapes
    num_rings = np.random.randint(1, 6)
    for _ in range(num_rings):
        outer_radius = np.random.randint(3, 7)
        inner_radius = outer_radius - np.random.randint(1, outer_radius)
        ring_color = np.random.choice(Color.NOT_BLACK)

        ring_shape = np.full((outer_radius * 2 + 1, outer_radius * 2 + 1), Color.BLACK)
        center = (outer_radius, outer_radius)
        
        # generate the outer and inner circles
        for i in range(outer_radius * 2 + 1):
            for j in range(outer_radius * 2 + 1):
                distance = np.sqrt((i - center[0])**2 + (j - center[1])**2)
                if inner_radius <= distance <= outer_radius:
                    ring_shape[i, j] = ring_color

        # place the ring in a random free location on the input grid with 1 cell padding
        try:
            x, y = random_free_location_for_sprite(input_grid, ring_shape, padding=1)
            blit_sprite(input_grid, ring_shape, x, y, background=Color.BLACK)
        except ValueError:
            continue
    
    return input_grid