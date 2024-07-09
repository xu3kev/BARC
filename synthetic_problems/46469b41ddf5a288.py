from common import *

import numpy as np
from typing import *

# concepts:
# patterns, positioning, copying, rotation, size

# description:
# In the input, you will see four square patterns of pixels in the corners of the grid. Each pattern is made of a single color, but different patterns may have different colors. The patterns may have different sizes.
# To make the output, copy each pattern to the corner diagonally opposite to its original position, rotating it 180 degrees. The output grid should be the same size as the input grid.

def main(input_grid):
    # get the patterns from the input
    objects = find_connected_components(input_grid, connectivity=8)

    # create the output grid with the same size as the input
    output_grid = np.full_like(input_grid, Color.BLACK)

    # copy and rotate each pattern
    for obj in objects:
        # crop the pattern to remove any extra rows or columns of black pixels
        sprite = crop(obj)
        
        # get the bounding box of the original pattern
        x, y, w, h = bounding_box(obj)
        
        # determine the new position (diagonally opposite)
        new_x = input_grid.shape[0] - x - w if x < input_grid.shape[0] // 2 else 0
        new_y = input_grid.shape[1] - y - h if y < input_grid.shape[1] // 2 else 0
        
        # rotate the sprite 180 degrees
        rotated_sprite = np.rot90(sprite, k=2)
        
        # copy the rotated pattern to the output grid
        blit_sprite(output_grid, rotated_sprite, x=new_x, y=new_y, background=Color.BLACK)
    
    return output_grid

def generate_input():
    # make a random sized grid with black background
    n = np.random.randint(8, 12)
    m = np.random.randint(8, 12)
    grid = np.zeros((n, m), dtype=int)

    # function to generate a random pattern
    def random_pattern(size):
        color = np.random.choice(list(Color.NOT_BLACK))
        return np.random.choice([color, Color.BLACK], size=(size, size))

    # generate patterns for each corner
    sizes = [np.random.randint(2, min(n, m) // 2) for _ in range(4)]
    
    # top-left corner
    grid[:sizes[0], :sizes[0]] = random_pattern(sizes[0])
    
    # top-right corner
    grid[:sizes[1], -sizes[1]:] = random_pattern(sizes[1])
    
    # bottom-left corner
    grid[-sizes[2]:, :sizes[2]] = random_pattern(sizes[2])
    
    # bottom-right corner
    grid[-sizes[3]:, -sizes[3]:] = random_pattern(sizes[3])

    # Check that at least one of the patterns is not all black
    # If they are all black, try again
    if np.all(grid == Color.BLACK):
        return generate_input()

    return grid