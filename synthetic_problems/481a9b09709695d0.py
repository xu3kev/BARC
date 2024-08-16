from common import *

import numpy as np
from typing import *

# concepts:
# objects, topology, growing

# description:
# In the input grid, you will see various colored objects on a black background. 
# To create the output grid, follow these steps:
# 1. For each object, determine if it's "hollow" (contains a fully-enclosed region).
# 2. If an object is hollow, fill its interior with its own color.
# 3. If an object is not hollow, grow it outwards by one pixel in all directions, without overlapping other objects.

def main(input_grid):
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=True)
    output_grid = np.full_like(input_grid, Color.BLACK)
    
    for obj in objects:
        color = obj[obj != Color.BLACK][0]  # Get the color of the object
        if is_hollow(obj):
            filled_obj = fill_hollow(obj, color)
        else:
            filled_obj = grow_object(obj, color, output_grid)
        
        blit_object(output_grid, filled_obj, background=Color.BLACK)
    
    return output_grid

def is_hollow(object):
    interior_mask = object_interior(object)
    object_mask = object != Color.BLACK
    hollow_mask = interior_mask & ~object_mask
    return np.any(hollow_mask)

def fill_hollow(obj, color):
    filled_obj = obj.copy()
    interior_mask = object_interior(obj)
    filled_obj[interior_mask] = color
    return filled_obj

def grow_object(obj, color, grid):
    grown_obj = np.full_like(grid, Color.BLACK)
    obj_mask = obj != Color.BLACK
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            shifted = np.roll(obj_mask, (dx, dy), axis=(0, 1))
            grown_obj[shifted & (grid == Color.BLACK)] = color
    return grown_obj

def generate_input():
    n = np.random.randint(15, 30)
    input_grid = np.full((n, n), Color.BLACK)
    colors = list(Color.NOT_BLACK)
    np.random.shuffle(colors)
    
    def random_object(hollow):
        size = np.random.randint(4, 8)
        obj = np.full((size, size), Color.BLACK)
        if hollow:
            obj[0, :] = obj[-1, :] = obj[:, 0] = obj[:, -1] = colors[0]
        else:
            mask = np.random.rand(size, size) < 0.7
            obj[mask] = colors[0]
        colors.append(colors.pop(0))  # Rotate colors
        return obj
    
    # Ensure at least one hollow and one non-hollow object
    for hollow in [True, False]:
        obj = random_object(hollow)
        try:
            x, y = random_free_location_for_sprite(input_grid, obj, padding=2)
            blit_sprite(input_grid, obj, x, y)
        except ValueError:
            return generate_input()
    
    # Add more random objects
    for _ in range(np.random.randint(2, 5)):
        obj = random_object(np.random.choice([True, False]))
        try:
            x, y = random_free_location_for_sprite(input_grid, obj, padding=2)
            blit_sprite(input_grid, obj, x, y)
        except ValueError:
            break
    
    return input_grid