from common import *

import numpy as np
from typing import *


# concepts:
# counting, surrounding, uniqueness

# description:
# In the input grid, there will be multiple 2x2 blue squares, multiple 2x2 red squares, and some red or blue dots sprinkled about.
# To make the output, count the number of 2x2 blue squares. Find the largest 2x2 blue square in terms of its bounding box dimensions
# and surround it with a border of green pixels. All other blue squares should be changed to black.

def main(input_grid):
    output_grid = input_grid.copy()

    # Find all 2x2 blue squares and keep track of their bounding boxes
    blue_squares = []
    for x in range(input_grid.shape[0]-1):
        for y in range(input_grid.shape[1]-1):
            if input_grid[x,y] == input_grid[x+1,y] == input_grid[x,y+1] == input_grid[x+1,y+1] == Color.BLUE:
                blue_squares.append((x, y, x+1, y+1))

    # Determining the largest 2x2 blue square by bounding box dimensions
    max_bb = (0, 0, 1, 1)  # This will store the largest blue square's bounding box
    for bb in blue_squares:
        x0, y0, x1, y1 = bb
        if (x1 - x0 + 1) * (y1 - y0 + 1) > (max_bb[2] - max_bb[0] + 1) * (max_bb[3] - max_bb[1] + 1):
            max_bb = bb

    # Surround the largest blue square with green pixels and turn others to black
    x0, y0, x1, y1 = max_bb
    for x in range(input_grid.shape[0]-1):
        for y in range(input_grid.shape[1]-1):
            if input_grid[x,y] == input_grid[x+1,y] == input_grid[x,y+1] == input_grid[x+1,y+1] == Color.BLUE:
                if (x, y, x+1, y+1) == max_bb:
                    for dx in range(-1, 3):
                        for dy in range(-1, 3):
                            if 0 <= x+dx < input_grid.shape[0] and 0 <= y+dy < input_grid.shape[1]:
                                if dx in (-1, 2) or dy in (-1, 2):
                                    output_grid[x+dx, y+dy] = Color.GREEN
                else:
                    output_grid[x:x+2, y:y+2] = Color.BLACK

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
    blue_pixel = np.full((1,1), Color.BLUE, dtype=int)
    for _ in range(np.random.randint(4)):
        x, y = random_free_location_for_sprite(grid, blue_pixel)
        blit_sprite(grid, blue_pixel, x, y)

    # make a random number of red pixel sprites and place them at random places on the grid
    red_pixel = np.full((1,1), Color.RED, dtype=int)
    for _ in range(np.random.randint(4)):
        x, y = random_free_location_for_sprite(grid, red_pixel)
        blit_sprite(grid, red_pixel, x, y)

    return grid