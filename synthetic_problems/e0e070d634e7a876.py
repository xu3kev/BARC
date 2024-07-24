from common import *

import numpy as np
from typing import *

# concepts:
# connectivity, objects, bounding box alignment

# description:
# In the input grid, you will see several disconnected objects of different colors. Each object is surrounded by black pixels (i.e., objects do not touch).
# Overlay each object's bounding box aligned at the top-left corner of the output grid.

def main(input_grid):
    # Find the connected components (objects) in the input_grid
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=4, background=Color.BLACK)
    
    # Create a blank output grid that is large enough to fit all objects aligned by their bounding boxes
    height, width = input_grid.shape
    output_grid = np.zeros((height, width), dtype=int)
    
    current_x, current_y = 0, 0
    
    for obj in objects:
        # Get the bounding box of the object
        x, y, obj_width, obj_height = bounding_box(obj, background=Color.BLACK)
        
        # Crop the object
        cropped_obj = crop(obj, background=Color.BLACK)
        
        # Ensure the object fits in the output grid
        if current_x + obj_height <= height and current_y + obj_width <= width:
            blit(output_grid, cropped_obj, current_x, current_y, background=Color.BLACK)
            current_y += obj_width  # Move to the next column
        else:
            current_x += obj_height
            current_y = 0  # Start from the first column again
            if current_x + obj_height <= height and current_y + obj_width <= width:
                blit(output_grid, cropped_obj, current_x, current_y, background=Color.BLACK)
                current_y += obj_width

    return output_grid


def generate_input():
    # Create a black grid of random size
    grid_size = np.random.randint(10, 20)
    grid = np.zeros((grid_size, grid_size), dtype=int)

    # Generate a few randomly colored objects
    num_objects = np.random.randint(3, 7)
    for i in range(num_objects):
        obj_shape = np.random.randint(2, 5)
        color = np.random.choice(list(Color.NOT_BLACK))
        obj = random_sprite(obj_shape, obj_shape, color_palette=[color], background=Color.BLACK)
        
        # Make sure objects do not touch
        x, y = random_free_location_for_object(grid, obj, border_size=1, padding=2)
        blit(grid, obj, x, y)
    
    return grid