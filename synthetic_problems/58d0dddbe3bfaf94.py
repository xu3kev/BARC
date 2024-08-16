from common import *

import numpy as np
from typing import *

# concepts:
# translating objects, upward movement

# description:
# Translate the single-colored object found in the input grid upwards by 2 rows.
# (If it doesn't fit, shift it as high as possible without losing any part.)

def main(input_grid):
    # Find the connected component, which is a monochromatic object
    object = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)[0]

    # Get the object's bounding box
    x, y, width, height = bounding_box(object, background=Color.BLACK)

    # Calculate new top-left position after translation
    new_x = max(0, x - 2)
    new_y = y

    # Create an output grid and translate the object upwards by 2 rows
    output_grid = np.zeros_like(input_grid)
    translated_object = translate(object, new_x - x, new_y - y, background=Color.BLACK)
    # Place the translated object onto the output grid
    blit(output_grid, translated_object, new_x, new_y)
    
    return output_grid

def generate_input():
    # Create a 10x10 grid of black (0)
    grid = np.zeros((10, 10), dtype=int)

    # Randomly generate a small contiguous shape (1 to 3 rows x 1 to 3 columns) with a random color
    object_height, object_width = np.random.randint(1, 4), np.random.randint(1, 4)
    random_color = random.choice(list(Color.NOT_BLACK))
    random_sprite_to_add = random_sprite(object_height, object_width, density=1, symmetry='not_symmetric', color_palette=[random_color])
    
    # Ensure the shape fits within the grid and place it randomly (with enough space for translation upward)
    max_x, max_y = 10 - object_height, 10 - object_width
    x, y = np.random.randint(0, max_x+1), np.random.randint(2, max_y+1)

    # Place the sprite on the grid
    blit(grid, random_sprite_to_add, x, y)
    
    return grid