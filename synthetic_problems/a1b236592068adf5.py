from common import *

import numpy as np
from typing import *

# concepts:
# grid mirroring, color guide, boundary detection

# description:
# In the input you will see an arbitrary shape (an object) positioned anywhere in the grid. You need to mirror this shape 
# along the middle of the grid both horizontally and vertically. The color of the mirrored shape should be the same as the object itself.

def main(input_grid):
    # Finding the bounding box of the object in the grid
    x, y, w, h = bounding_box(input_grid, background=Color.BLACK)
    
    # Extracting the object
    object = input_grid[x:x+w, y:y+h]
    
    # Creating output grid
    output_grid = np.copy(input_grid)
    
    # Finding the center of the input grid
    center_x, center_y = output_grid.shape[0] // 2, output_grid.shape[1] // 2
    
    # Mirroring horizontally and vertically
    mirrored_object_h = np.flipud(object)
    mirrored_object_v = np.fliplr(object)
    mirrored_object_hv = np.flipud(np.fliplr(object))
    
    # Blit the original and mirrored objects onto the output grid
    blit(output_grid, object, center_x - w//2, center_y - h//2, background=Color.BLACK)
    blit(output_grid, mirrored_object_h, output_grid.shape[0] - center_x - w//2, center_y - h//2, background=Color.BLACK)
    blit(output_grid, mirrored_object_v, center_x - w//2, output_grid.shape[1] - center_y - h//2, background=Color.BLACK)
    blit(output_grid, mirrored_object_hv, output_grid.shape[0] - center_x - w//2, output_grid.shape[1] - center_y - h//2, background=Color.BLACK)
    
    return output_grid

def generate_input():
    # Create a stochastic grid size between 10x10 to 20x20
    n, m = np.random.randint(10, 21), np.random.randint(10, 21)
    grid = np.zeros((n, m), dtype=int)
    
    # Generate a random sprite with random color
    sprite_size = np.random.randint(3, min(n, m)//2)
    sprite = random_sprite(sprite_size, sprite_size, symmetry='not_symmetric', color_palette=[random.choice(list(Color.NOT_BLACK))])
    
    # Place the sprite at a random position in the grid
    x, y = random_free_location_for_object(grid, sprite, border_size=2)
    blit(grid, sprite, x, y, background=Color.BLACK)
    
    return grid