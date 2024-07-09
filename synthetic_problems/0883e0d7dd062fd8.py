from common import *

import numpy as np
from typing import *

# concepts:
# alignment, scaling, rotation

# description:
# In the input, you will see several objects of different colors, each within its own rectangular bounding box.
# The goal is to first scale each object up by a factor of 2 along both dimensions and then rotate each scaled object 90 degrees clockwise. 
# Place the transformed objects into a larger output grid such that their relative positions are preserved.

def main(input_grid):
    output_grid_size_factor = 2
    rotation_degree = 90
    
    # Step 1: Extract all objects from the input grid
    objects = detect_objects(input_grid, background=Color.BLACK, monochromatic=False, connectivity=8)
    
    # Step 2: Determine the size of the output grid
    input_shape = input_grid.shape
    output_shape = (input_shape[0] * output_grid_size_factor, input_shape[1] * output_grid_size_factor)
    output_grid = np.full(output_shape, Color.BLACK, dtype=int)
    
    def rotate_clockwise_90(sprite):
        return np.rot90(sprite, k=3)

    def scale_up(sprite, factor):
        return np.kron(sprite, np.ones((factor, factor), dtype=int))
    
    # Step 3: Process and place each object
    for obj in objects:
        color = np.unique(obj[obj != Color.BLACK])[0]
        scaled_obj = scale_up(obj, output_grid_size_factor)
        rotated_obj = rotate_clockwise_90(scaled_obj)
        
        # Find the original bounding box in the input grid
        x, y, w, h = bounding_box(obj)

        # Calculate the new position for the transformed object in the output grid
        delta_x, delta_y = w, h
        new_x, new_y = (x + delta_x) * output_grid_size_factor, (y + delta_y) * output_grid_size_factor
        
        # Blit the rotated object into the output grid
        blit(output_grid, rotated_obj, new_x, new_y)
    
    return output_grid


def generate_input():
    # Define the input grid size
    n, m = np.random.randint(8, 12, 2)
    input_grid = np.full((n, m), Color.BLACK, dtype=int)
    
    num_objects = np.random.randint(3, 5)
    
    for _ in range(num_objects):
        # Generate a random small sprite
        w, h = np.random.randint(2, 4, 2)
        color = np.random.choice(list(Color.NOT_BLACK))
        sprite = random_sprite(w, h, color_palette=[color])
        
        # Place the sprite on the grid at a random free location
        x, y = random_free_location_for_object(input_grid, sprite, padding=1)
        blit(input_grid, sprite, x, y)
    
    return input_grid