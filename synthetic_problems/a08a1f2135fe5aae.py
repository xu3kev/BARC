from common import *

import numpy as np
from typing import *

# concepts:
# alignment by color, pixel manipulation, objects

# description:
# In the input grid, you will see several disjoint objects of random shapes and colors, each containing a single BLUE pixel. 
# To create the output, align all objects so that their BLUE pixels overlap at the center of the grid. The output grid will be cropped to the minimum size 
# that contains all the objects, and all BLUE pixels should align. Make sure the output grid is centered around the aligned BLUE pixels.

def main(input_grid):
    # 1. Extract the objects from the input grid
    objects = find_connected_components(input_grid, background=Color.BLACK, monochromatic=False, connectivity=8)

    # 2. Make a suitably large output grid
    output_grid = np.full((input_grid.shape[0]*2, input_grid.shape[1]*2), Color.BLACK, dtype=int)

    # 3. Place each object so that the BLUE pixel aligns to the center of the output grid
    for obj in objects:
        # Crop the object to create a sprite
        sprite = crop(obj, background=Color.BLACK)
        
        # Identify the coordinates of the BLUE pixel
        blue_pixel = np.argwhere(sprite == Color.BLUE)[0]
        sprite_x, sprite_y = blue_pixel

        # Center of the output grid
        center_x, center_y = output_grid.shape[0] // 2, output_grid.shape[1] // 2

        # Calculate top-left coordinates to place the sprite such the BLUE pixel aligns with our target center
        x_offset, y_offset = center_x - sprite_x, center_y - sprite_y

        # Blit the sprite onto the output grid at the calculated location
        blit_sprite(output_grid, sprite, x_offset, y_offset, background=Color.BLACK)
    
    # 4. Crop the output grid to remove excessive black space
    output_grid = crop(output_grid, background=Color.BLACK)

    return output_grid


def generate_input():
    input_grid_shape = (10, 10)
    input_grid = np.zeros(input_grid_shape, dtype=int)

    # Create disjoint objects each containing a single BLUE pixel randomly positioned within it
    num_objects = np.random.randint(2, 5)
    for _ in range(num_objects):
        # Random shape dimensions between 2x2 and 4x4
        shape_dims = (np.random.randint(2, 5), np.random.randint(2, 5))
        object_color = np.random.choice(list(Color.NOT_BLACK))

        # Create a random object with a single BLUE pixel at a random position
        obj = np.full(shape_dims, object_color, dtype=int)
        obj[np.random.randint(shape_dims[0]), np.random.randint(shape_dims[1])] = Color.BLUE

        # Place the object in a random free location within the input grid
        x, y = random_free_location_for_sprite(input_grid, obj, padding=1)
        blit_sprite(input_grid, obj, x, y)
    
    return input_grid