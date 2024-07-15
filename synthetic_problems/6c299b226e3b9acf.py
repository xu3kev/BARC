from common import *

import numpy as np
from typing import *

# concepts:
# objects, counting, color, position-based transformation

# description:
# In the input you will see grey objects on a black background.
# Depending on their position in the grid, color the objects:
# - Objects in the left half of the grid (x < grid_width / 2) should be colored RED if they consist of two pixels, GREEN if they consist of three pixels, and BLUE if they consist of four pixels.
# - Objects in the right half of the grid (x >= grid_width / 2) should be colored ORANGE if they consist of two pixels, PINK if they consist of three pixels, and YELLOW if they consist of four pixels.

def main(input_grid: np.ndarray) -> np.ndarray:
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)
    grid_width = input_grid.shape[1]

    # get the objects in the input grid
    objects = find_connected_components(input_grid)

    # count the number of pixels in each object and color them accordingly
    for obj in objects:
        obj_bbox = bounding_box(obj)
        num_pixels = np.sum(obj == Color.GREY)
        
        if obj_bbox[0] < grid_width / 2:  # left half of the grid
            if num_pixels == 2:
                color = Color.RED
            elif num_pixels == 3:
                color = Color.GREEN
            elif num_pixels == 4:
                color = Color.BLUE
            else:
                color = Color.GREY
        else:  # right half of the grid
            if num_pixels == 2:
                color = Color.ORANGE
            elif num_pixels == 3:
                color = Color.PINK
            elif num_pixels == 4:
                color = Color.YELLOW
            else:
                color = Color.GREY

        output_grid[obj == Color.GREY] = color

    return output_grid

def generate_input() -> np.ndarray:
    # make a black 10x20 grid as the background
    n, m = 10, 20
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