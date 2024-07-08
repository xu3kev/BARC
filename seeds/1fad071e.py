from common import *

import numpy as np
from typing import *

# concepts:
# counting

# description:
# In the input you will see multiple 2x2 blue squares, multiple 2x2 red squares, and some red or blue dots sprinkled about.
# To make the output, fill a 1x5 grid with blue pixels from left to right for each 2x2 blue square in the input (counting the number of blue 2x2 squares).

def main(input_grid):
    # make a counter to count the number of blue squares
    blue_square_count = 0

    # scan the grid for blue squares and count them up
    for x in range(input_grid.shape[0]-1):
        for y in range(input_grid.shape[1]-1):
            if input_grid[x,y] == input_grid[x+1,y] == input_grid[x,y+1] == input_grid[x+1,y+1] == Color.BLUE:
                blue_square_count += 1
    
    # make a 1x5 output grid
    output_grid = np.zeros((5,1), dtype=int)

    # add the number of blue squares to the array from left to right with each pixel representing one blue block
    output_grid[:blue_square_count, :] = Color.BLUE

    return output_grid

def generate_input():
    # make 9x9 black background grid first
    n = m = 9
    grid = np.zeros((n,m), dtype=int)

    # make a random number of blue square sprites and place them at random places on the grid but don't have them touch
    blue_square = np.full((2,2), Color.BLUE, dtype=int)
    for _ in range(np.random.randint(2,6)):
        x, y = random_free_location_for_sprite(grid, blue_square)
        if not contact(object1=grid, object2=blue_square, x2=x, y2=y): # only place new squares that won't touch old ones
          blit_sprite(grid, blue_square, x, y)
    
    # make a random number of red square sprites and place them at random places on the grid but don't have them touch
    red_square = np.full((2,2), Color.RED, dtype=int)
    for _ in range(np.random.randint(2,6)):
        x, y = random_free_location_for_sprite(grid, red_square)
        if not contact(object1=grid, object2=red_square, x2=x, y2=y): # only place new squares that won't touch old ones
          blit_sprite(grid, red_square, x, y)
        
    # make a random number of blue pixel sprites and place them at random places on the grid
    blue_pixel = random_sprite(1, 1, density=1, color_palette=[Color.BLUE])
    for _ in range(np.random.randint(4)):
        x, y = random_free_location_for_sprite(grid, blue_pixel)
        blit_sprite(grid, blue_pixel, x, y)

    # make a random number of red pixel sprites and place them at random places on the grid
    red_pixel = random_sprite(1, 1, density=1, color_palette=[Color.RED])
    for _ in range(np.random.randint(4)):
        x, y = random_free_location_for_sprite(grid, red_pixel)
        blit_sprite(grid, red_pixel, x, y)

    return grid




# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)