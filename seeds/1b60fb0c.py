from common import *

import numpy as np
from typing import *

# concepts:
# symmetry

# description:
# In the input you will see an image containing blue pixels that is almost rotationally symmetric, except that it is missing the section either north, south, east, or west that would make it rotationally symmetric
# Color red all the pixels that would need to be colored in order to make the image rotationally symmetric (when rotating clockwise)

def main(input_grid):

    # The goal is to make the object rotationally symmetric, *not* to make the whole grid rotationally symmetric
    # We have to extract the object from the grid and then rotate it to construct the missing section
    blue_sprite = crop(input_grid)
    rotated_blue_sprite = np.rot90(blue_sprite)
    
    # We need to find the optimal location for placing the rotated sprite
    # This will make the resulting object radially symmetric
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            
            test_grid = np.copy(input_grid)
            blit_sprite(test_grid, rotated_blue_sprite, x, y, background=Color.BLACK)
            test_blue_sprite = crop(test_grid)

            # Check if the resulting object is radially symmetric
            if np.array_equal(test_blue_sprite, np.rot90(test_blue_sprite)):
                # Save what the input would look like if it were perfectly symmetric
                perfectly_symmetric_grid = test_grid
                break

    # The missing section is the part of the input grid that would have been blue if it were perfectly symmetric
    missing_pixels = np.where((input_grid == Color.BLACK) & (perfectly_symmetric_grid == Color.BLUE))

    # Color the missing section red
    output_grid = np.copy(input_grid)
    output_grid[missing_pixels] = Color.RED

    return output_grid

def main(input_grid):
    # This also works, and uses the library function `detect_rotational_symmetry``
    
    # Plan:
    # 1. Detect the (x,y) point that the object is rotated around
    # 2. Rotate each blue colored pixel around that point. If the rotated pixel is not colored, color it red.

    output_grid = np.copy(input_grid)

    # Find the symmetry
    sym = detect_rotational_symmetry(input_grid, ignore_colors=[Color.BLACK], background=Color.BLACK)
    
    # Rotate the blues and color red as needed
    blues = np.argwhere(input_grid == Color.BLUE)
    for x, y in blues:
        rotated_x, rotated_y = sym.apply(x, y, iters=1)        

        if input_grid[rotated_x, rotated_y] == Color.BLACK:
            output_grid[rotated_x, rotated_y] = Color.RED
    
    return output_grid

def generate_input():
    # make a black medium large grid
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # make a blue radially symmetric sprite and put it at a random free location
    sprite_size = np.random.randint(8, min(n, m))
    sprite = random_sprite(sprite_size, sprite_size, symmetry='radial', color_palette=[Color.BLUE], density=0.2)
    x, y = random_free_location_for_sprite(grid, sprite)

    # remove a random section of the sprite to make it not radially symmetric
    remove_length = np.random.randint(1, sprite_size//4)
    quadrant = np.random.choice(['north', 'south', 'east', 'west'])
    if quadrant == 'north':
        sprite[sprite_size//2 - remove_length : sprite_size//2 + remove_length, : sprite_size//2] = Color.BLACK
    elif quadrant == 'south':
        sprite[sprite_size//2 - remove_length : sprite_size//2 + remove_length, sprite_size//2 :] = Color.BLACK
    elif quadrant == 'east':
        sprite[: sprite_size//2, sprite_size//2 - remove_length : sprite_size//2 + remove_length] = Color.BLACK
    elif quadrant == 'west':
        sprite[sprite_size//2 :, sprite_size//2 - remove_length : sprite_size//2 + remove_length] = Color.BLACK

    blit_sprite(grid, sprite, x, y)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)