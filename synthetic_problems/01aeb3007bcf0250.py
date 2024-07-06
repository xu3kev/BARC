from common import *

import numpy as np
from typing import *

# concepts:
# reflection, vertical axis, mirroring

# description:
# In the input, you will see several shapes of different colors.
# The goal is to create the mirror image of each shape along the vertical axis.

def main(input_grid):
    # Get the dimensions of the input grid
    n, m = input_grid.shape
    
    # Prepare the output grid of the same size
    output_grid = np.zeros((n, m), dtype=int)
    
    # Find all the objects in the input grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)
    
    for obj in objects:
        # Get the bounding box of the object
        x, y, w, h = bounding_box(obj)
        
        # Extract the object itself
        cropped = crop(obj)
        
        # Mirror the object along the vertical axis
        mirrored = np.fliplr(cropped)
        
        # Place the mirrored object into a position symmetric across the vertical axis in the output grid
        output_x = n - x - h
        output_y = m - y - w
        
        blit(output_grid, mirrored, output_x, output_y)
    
    return output_grid

def generate_input():
    # Random grid dimensions
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    
    # Create a blank grid
    grid = np.zeros((n, m), dtype=int)
    
    # Number of objects to create
    num_objects = np.random.randint(2, 5)
    
    for _ in range(num_objects):
        # Random size for the object
        obj_size_x, obj_size_y = np.random.randint(2, 5), np.random.randint(2, 5)
        
        # Create a random monochromatic object
        color = np.random.choice(Color.NOT_BLACK)
        obj = np.full((obj_size_x, obj_size_y), color)
        
        # Place the object in a random location
        x, y = random_free_location_for_object(grid, obj, padding=1)
        blit(grid, obj, x, y)
    
    return grid