from common import *

import numpy as np
from typing import *

# concepts:
# rotating objects, finding connected components

# description:
# Given an input grid with isolated, colored shapes. To produce the output,
# identify these shapes, rotate each shape 90 degrees clockwise, and place them back on the grid.
# Ensure that no two shapes overlap after rotation. 

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.zeros_like(input_grid)
    
    # Find all isolated shapes
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)
    
    for obj in objects:
        # Rotate each shape 90 degrees clockwise
        rotated_obj = np.rot90(obj, k=-1)
        
        # Find a random free location for the rotated object
        x, y = random_free_location_for_object(output_grid, rotated_obj)
        
        # Blit the rotated object onto the output grid
        blit(output_grid, rotated_obj, x, y)
        
    return output_grid

def generate_input() -> np.ndarray:
    grid_size = 10
    grid = np.zeros((grid_size, grid_size), dtype=int)

    # Number of objects to create
    num_objects = np.random.randint(1, 4)
    
    for _ in range(num_objects):
        # Generate a small random sprite
        sprite_dim = np.random.randint(2, 4)
        sprite = random_sprite(sprite_dim, sprite_dim, color_palette=Color.NOT_BLACK, symmetry='not_symmetric')
        
        # Find a random location to place the sprite
        x, y = random_free_location_for_object(grid, sprite)
        
        # Place the sprite on the grid
        blit(grid, sprite, x, y)
    
    return grid