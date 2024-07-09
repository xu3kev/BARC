from common import *

import numpy as np
from typing import *

# concepts:
# objects, counting, color

# description:
# In the input you will see grey objects on a black background.
# To make the output, count the number of pixels in each object and color the object green if it has two pixels, red if it has three pixels, and blue if it has four pixels.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # get the objects in the input grid
    objects = find_connected_components(input_grid)

    # count the number of pixels in each object and color them accordingly
    for obj in objects:
        num_pixels = np.sum(obj == Color.GREY)
        if num_pixels == 2:
            color = Color.GREEN
        elif num_pixels == 3:
            color = Color.RED
        elif num_pixels == 4:
            color = Color.BLUE
        else:
            color = Color.GREY
        output_grid[obj == Color.GREY] = color

    return output_grid

def generate_input():
    # make a black 10x10 grid as the background
    n = m = 10
    grid = np.zeros((n, m), dtype=int)
    
    # make a random number of sprites
    num_sprites = np.random.randint(3, 7)
    for _ in range(num_sprites):
        sprite = random_sprite(np.random.randint(1, 4), np.random.randint(1, 4), symmetry="not_symmetric", color_palette=[Color.GREY])
        # make sure the sprite has between 2 and 4 pixels
        while np.sum(sprite == Color.GREY) < 2 or np.sum(sprite == Color.GREY) > 4:
            sprite = random_sprite(np.random.randint(1, 4), np.random.randint(1, 4), symmetry="not_symmetric", color_palette=[Color.GREY])
        try:
            x, y = random_free_location_for_sprite(grid, sprite, padding=1, padding_connectivity=8)
            blit_sprite(grid, sprite, x=x, y=y)
        except:
            pass

    return grid













# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)