from common import *

import numpy as np
from typing import *

# concepts:
# symmetry detection, occlusion, repetition

# description:
# In the input, you will see a 15x15 grid with a partially occluded rotationally symmetric object.
# The object is made up of 3 identical sprites, each rotated 120 degrees from each other around a central point.
# Some parts of the object are covered by black pixels.
# To make the output:
# 1. Detect the rotational symmetry and center of the object.
# 2. Identify one of the three identical sprites that make up the object.
# 3. Rotate this sprite to fill in the missing parts and complete the object.
# 4. Repeat the completed object twice more, placing the copies in the top-left and bottom-right corners of the grid.

def main(input_grid):
    output_grid = np.full_like(input_grid, Color.BLACK)
    
    # Detect rotational symmetry
    sym = detect_rotational_symmetry(input_grid, ignore_colors=[Color.BLACK])
    
    # Find all non-black pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    
    # Complete the object
    for x, y in colored_pixels:
        color = input_grid[x, y]
        for i in range(3):
            rotated_x, rotated_y = sym.apply(x, y, iters=i)
            output_grid[rotated_x, rotated_y] = color
    
    # Crop the completed object
    completed_object = crop(output_grid, background=Color.BLACK)
    
    # Place the object in the center of the output grid
    center_x, center_y = output_grid.shape[0] // 2, output_grid.shape[1] // 2
    object_center_x, object_center_y = completed_object.shape[0] // 2, completed_object.shape[1] // 2
    blit_sprite(output_grid, completed_object, center_x - object_center_x, center_y - object_center_y)
    
    # Place copies in top-left and bottom-right corners
    blit_sprite(output_grid, completed_object, 0, 0)
    blit_sprite(output_grid, completed_object, output_grid.shape[0] - completed_object.shape[0], output_grid.shape[1] - completed_object.shape[1])
    
    return output_grid

def generate_input():
    grid = np.full((15, 15), Color.BLACK, dtype=int)
    
    # Create a small sprite
    sprite = random_sprite(3, 3, density=0.7, color_palette=list(Color.NOT_BLACK))
    
    # Create the rotationally symmetric object
    object_grid = np.full((7, 7), Color.BLACK, dtype=int)
    center = object_grid.shape[0] // 2
    
    for i in range(3):
        rotated_sprite = np.rot90(sprite, k=i)
        x, y = center - 1, center - 1
        blit_sprite(object_grid, rotated_sprite, x, y)
    
    # Randomly remove some pixels
    mask = np.random.choice([True, False], size=object_grid.shape, p=[0.3, 0.7])
    object_grid[mask] = Color.BLACK
    
    # Place the object in the center of the input grid
    x, y = grid.shape[0] // 2 - object_grid.shape[0] // 2, grid.shape[1] // 2 - object_grid.shape[1] // 2
    blit_sprite(grid, object_grid, x, y)
    
    return grid