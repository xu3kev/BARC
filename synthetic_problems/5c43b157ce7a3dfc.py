from common import *

import numpy as np
from typing import *

# concepts:
# patterns, objects, object scaling

# description:
# In the input, you are given a grid with several colored objects. Each object is of the same color but their shapes may vary.
# To create the output, you need to scale each object by a factor of 2, maintaining the same shape and relative position within the grid.

def main(input_grid):
    # Detect all objects in the grid, assuming they do not overlap and each is monochromatic
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)
    
    # Create an empty grid for the output of double the dimensions of the input grid
    output_grid = np.full((input_grid.shape[0] * 2, input_grid.shape[1] * 2), Color.BLACK)
    
    for obj in objects:
        # Determine the bounding box to locate the object within the input grid
        x, y, width, height = bounding_box(obj, background=Color.BLACK)
        
        # Scale the object by a factor of 2
        scaled_obj = np.repeat(np.repeat(obj[x:x+width, y:y+height], 2, axis=0), 2, axis=1)
        
        # Place the scaled object at the double its original position in the output grid
        blit(output_grid, scaled_obj, x * 2, y * 2, background=Color.BLACK)
    
    return output_grid

def generate_input():
    # Initialize a random size for the grid
    rows = np.random.randint(5, 10)
    cols = np.random.randint(5, 10)
    
    # Initialize the grid with black background
    grid = np.full((rows, cols), Color.BLACK)
    
    # Number of objects
    num_objects = np.random.randint(1, 5)
    
    for _ in range(num_objects):
        # Generate a random object
        obj = random_sprite(n=[1, 2, 3], m=[1, 2, 3], color_palette=Color.NOT_BLACK)
        
        # Find a free location to place the object
        x, y = random_free_location_for_object(grid, obj, background=Color.BLACK, border_size=1)
        
        # Place the object in the grid
        blit(grid, obj, x, y)

    return grid