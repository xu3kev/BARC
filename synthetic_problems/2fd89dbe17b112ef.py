from common import *

import numpy as np
from typing import *

# concepts:
# rotation, pixel manipulation, object detection

# description:
# In the input, you will see an object in a rectangular grid. 
# The task is to rotate this object 90 degrees clockwise around its own center of mass to form the output grid. 
# If the rotated object goes out of bounds, truncate it.

def main(input_grid):
    objects = detect_objects(input_grid, monochromatic=False, connectivity=8, background=Color.BLACK)
    if not objects:
        return input_grid
    obj = objects[0]  # assume there's only one object for simplicity

    # Get the bounding box of the object
    x, y, width, height = bounding_box(obj, background=Color.BLACK)

    # Crop the object from the input grid
    cropped_obj = crop(input_grid[x:x+width, y:y+height], background=Color.BLACK)

    # Create an empty output grid
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)

    # Compute the center of the object
    center_x = width // 2
    center_y = height // 2

    # Rotate the object 90 degrees clockwise
    for i in range(width):
        for j in range(height):
            if cropped_obj[i, j] != Color.BLACK:
                new_x = center_y - (j - center_y)
                new_y = center_x + (i - center_x)
                new_x += (m - width) // 2  # Center the object
                new_y += (n - height) // 2  # Center the object
                if 0 <= new_x < n and 0 <= new_y < m:
                    output_grid[new_x, new_y] = cropped_obj[i, j]

    return output_grid

def generate_input():
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    # Random object color
    object_color = np.random.choice(Color.NOT_BLACK)

    # Randomly generate an object (a sprite)
    sprite = random_sprite(np.random.randint(3, 7), np.random.randint(3, 7), density=0.6, color_palette=[object_color])
    sprite_x, sprite_y = random_free_location_for_object(grid, sprite)

    blit(grid, sprite, sprite_x, sprite_y)
    return grid