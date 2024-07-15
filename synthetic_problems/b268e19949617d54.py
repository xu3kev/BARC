from common import *

import numpy as np
from typing import *

# concepts:
# reflection, objects

# description:
# In the input, you will see several small colored shapes (objects) scattered on a black background.
# To make the output, reflect each object horizontally about its own vertical center axis.
# The positions of the objects should remain the same, only their internal structure changes.

def main(input_grid):
    # Find all objects in the input grid
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)
    
    # Create an output grid with the same dimensions as the input
    output_grid = np.full_like(input_grid, Color.BLACK)
    
    for obj in objects:
        # Crop the object to remove surrounding black pixels
        cropped_obj = crop(obj, background=Color.BLACK)
        
        # Reflect the cropped object horizontally
        reflected_obj = cropped_obj[:, ::-1]
        
        # Find the original position of the object in the input grid
        y, x = np.where(obj != Color.BLACK)
        top_left_y, top_left_x = y.min(), x.min()
        
        # Place the reflected object at its original position in the output grid
        blit_sprite(output_grid, reflected_obj, x=top_left_x, y=top_left_y, background=Color.BLACK)
    
    return output_grid

def generate_input():
    # Create a black background grid
    n, m = np.random.randint(15, 25), np.random.randint(15, 25)
    grid = np.full((n, m), Color.BLACK)
    
    # Generate 2-4 random objects
    num_objects = np.random.randint(2, 5)
    
    for _ in range(num_objects):
        # Create a random sprite (object)
        obj_size = np.random.randint(3, 6)
        obj = random_sprite(obj_size, obj_size, density=0.7, symmetry="not_symmetric", color_palette=Color.NOT_BLACK)
        
        # Find a random free location for the object
        try:
            x, y = random_free_location_for_sprite(grid, obj, background=Color.BLACK, padding=1, border_size=1)
            blit_sprite(grid, obj, x, y, background=Color.BLACK)
        except:
            continue
    
    # Ensure we have at least one object
    if np.all(grid == Color.BLACK):
        return generate_input()
    
    return grid