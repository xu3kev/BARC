from common import *

import numpy as np
from typing import *

# concepts:
# objects, symmetry detection, pixel manipulation, connecting colors

# description:
# In the input you will see a grid with multiple monochromatic objects in different colors. Some objects have parts of another color attached to them.
# To make the output:
# 1. Identify the main color of each object.
# 2. Replace each object with its mirror image across the central vertical axis of the grid.
# 3. The attached pixels (of a different color) should remain attached to the mirrored object.

def main(input_grid):
    # Identify the background color
    background_color = np.bincount(input_grid.flatten()).argmax()

    # Find all connected components
    objects = find_connected_components(input_grid, background=background_color, connectivity=8, monochromatic=False)
    
    # Prepare the output grid with the same shape as input, filled with background color
    output_grid = np.full_like(input_grid, background_color)
    
    # Loop through each object and process
    for obj in objects:
        # Get the bounding box of the object
        x, y, width, height = bounding_box(obj, background=background_color)
        
        # Extract the object sprite and mirror it horizontally
        obj_sprite = crop(obj[x:x+width, y:y+height], background=background_color)
        mirrored_sprite = np.fliplr(obj_sprite)
        
        # Determine the mirrored position in the output grid
        mirrored_x = x
        mirrored_y = input_grid.shape[1] - (y + width)
        
        # Blit the mirrored sprite onto the output grid
        blit_sprite(output_grid, mirrored_sprite, mirrored_x, mirrored_y, background=background_color)
    
    return output_grid


def generate_input():
    grid_size = 20
    grid = np.full((grid_size, grid_size), Color.BLACK)
    
    num_objects = np.random.randint(3, 6)
    for _ in range(num_objects):
        # Create a random monochromatic object
        obj_size = np.random.randint(2, 5)
        obj_color = np.random.choice(Color.NOT_BLACK)
        obj = random_sprite(obj_size, obj_size, symmetry="not_symmetric", color_palette=[obj_color])
        
        # Randomly attach some pixels of another color
        attach_color = np.random.choice(list(set(Color.NOT_BLACK) - {obj_color}))
        attach_points = np.random.randint(1, 4)
        for _ in range(attach_points):
            ax, ay = np.random.randint(0, obj_size, size=2)
            obj[ax, ay] = attach_color
        
        # Place the object randomly in the grid
        x, y = random_free_location_for_sprite(grid, obj, padding=1, border_size=1, background=Color.BLACK)
        blit_sprite(grid, obj, x, y)

    return grid