from common import *

import numpy as np
from typing import *

# concepts:
# edge detection, border coloring

# description:
# In the input you will see multiple colored shapes. 
# Each shape is composed of contiguous pixels of the same color. 
# The transformation involves detecting the edges of each shape and coloring these edges with one specific color (let's pick RED). 
# The interior of the shapes remains unchanged.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Detect all the objects in the grid
    objects = detect_objects(output_grid, background=Color.BLACK, monochromatic=True, connectivity=4)
    
    for obj in objects:
        # Get the boundary of the object
        boundary_mask = object_boundary(obj, background=Color.BLACK)
        
        # Find the position of the boundary pixels
        boundary_positions = np.argwhere(boundary_mask)
        
        for (x, y) in boundary_positions:
            # Color the boundary pixels red in the output grid
            output_grid[x, y] = Color.RED
    
    return output_grid

def generate_input():
    grid = np.zeros((20, 20), dtype=int)
    num_shapes = np.random.randint(1, 4)

    for _ in range(num_shapes):
        # Generate a random sprite with random size
        sprite_size = np.random.randint(3, 8)
        sprite_color = random.choice(list(Color.NOT_BLACK))
        sprite = random_sprite(sprite_size, sprite_size, color_palette=[sprite_color], connectivity=4, density=0.6)
        
        # Find a random free location and blit the sprite on the grid
        x, y = random_free_location_for_object(grid, sprite, background=Color.BLACK)
        blit(grid, sprite, x, y)

    return grid