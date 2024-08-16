from common import *

import numpy as np
from typing import *

# concepts:
# objects, connectivity, resizing

# description:
# In the input grid, various colored objects (connected components) are scattered. 
# Each object should be identified and then shrunk by 1 pixel breadth-width at each border.
# If an object becomes smaller than a single pixel, it should disappear.

def main(input_grid):
    objects = find_connected_components(input_grid, connectivity=4)
    output_grid = np.full_like(input_grid, Color.BLACK)
    
    for obj in objects:
        # Detect bounds and shrink it by replacing the boundary pixels with the background color
        object_mask = obj != Color.BLACK
        
        for _ in range(1):
            boundary_mask = object_boundary(object_mask, background=0)
            object_mask[boundary_mask] = 0
        
        # Reconstruct object and place it on the output grid
        reconstructed_object = input_grid * object_mask
        
        blit(output_grid, reconstructed_object, background=Color.BLACK)

    return output_grid

def generate_input():
    n = np.random.randint(10, 15)
    input_grid = np.full((n, n), Color.BLACK)
    
    def random_object():
        color = np.random.choice(list(Color.NOT_BLACK))
        height, width = np.random.randint(3, 7, size=2)
        obj = np.full((height, width), color)
        return obj
    
    num_objects = np.random.randint(5, 10)
    for _ in range(num_objects):
        obj = random_object()
        try:
            x, y = random_free_location_for_object(input_grid, obj, padding=1)
            blit(input_grid, obj, x, y)
        except ValueError:
            pass  # Skip if there is no space left to put objects
            
    return input_grid