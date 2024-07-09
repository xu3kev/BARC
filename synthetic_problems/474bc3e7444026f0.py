from common import *

import numpy as np
from typing import *

# concepts:
# reflection, symmetry, objects

# description:
# In the input, you will see a rectangular grid with one or two randomly colored objects.
# To make the output:
# 1. Reflect the entire grid horizontally.
# 2. For each object in the original input:
#    a. If the object has horizontal symmetry, leave it as is.
#    b. If the object doesn't have horizontal symmetry, replace it with its vertically reflected version.
# The background should remain black.

def main(input_grid):
    # Reflect the entire grid horizontally
    output_grid = np.flip(input_grid, axis=1)
    
    # Find objects in the original input
    objects = find_connected_components(input_grid, monochromatic=False, background=Color.BLACK)
    
    for obj in objects:
        # Get the bounding box of the object
        x, y, w, h = bounding_box(obj)
        
        # Check if the object has horizontal symmetry
        is_horizontally_symmetric = np.array_equal(obj, np.flip(obj, axis=1))
        
        if not is_horizontally_symmetric:
            # If not symmetric, replace with vertically reflected version
            reflected_obj = np.flip(obj, axis=0)
            blit_object(output_grid, reflected_obj, background=Color.BLACK)
        else:
            # If symmetric, leave as is (it's already reflected in the output_grid)
            pass
    
    return output_grid

def generate_input():
    # Create a rectangular grid
    n, m = np.random.randint(8, 15), np.random.randint(8, 15)
    grid = np.full((n, m), Color.BLACK)
    
    # Generate 1 or 2 random objects
    num_objects = np.random.randint(1, 3)
    for _ in range(num_objects):
        obj_size = np.random.randint(3, 6)
        obj = random_sprite(obj_size, obj_size, density=0.7, symmetry=None, color_palette=Color.NOT_BLACK)
        
        # Find a free location for the object
        x, y = random_free_location_for_sprite(grid, obj, padding=1, border_size=1)
        
        # Place the object on the grid
        blit_sprite(grid, obj, x, y)
    
    return grid