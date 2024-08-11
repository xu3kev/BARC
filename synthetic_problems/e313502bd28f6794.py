from common import *

import numpy as np
from typing import *

# concepts:
# patterns, repetition, sliding objects

# description:
# In the input grid, you will see a block-like pattern made up of multiple colors. 
# This pattern must be identified and selected.
# The transformation involves sliding the entire pattern to the following corner: 
# If the pattern is in the top-left corner, slide it to the bottom-right corner.
# If the pattern is in the top-right corner, slide it to the bottom-left corner.
# If the pattern is in the bottom-left corner, slide it to the top-right corner.
# If the pattern is in the bottom-right corner, slide it to the top-left corner.
# The output grid should have these pattern blocks slid to their new positions while everything else remains the same.

def main(input_grid):
    # find the patterns in the input
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)
    
    # creating a copy of the input grid to manipulate and generate the output grid
    output_grid = np.copy(input_grid)

    # boundaries for the four quadrants
    middle_x, middle_y = input_grid.shape[0] // 2, input_grid.shape[1] // 2

    for obj in objects:
        # determine the bounding box of each pattern
        top, left, width, height = bounding_box(obj)
        
        # determine the new position based on the starting corner of the pattern
        if (top < middle_x) and (left < middle_y):  # top-left corner
            new_top, new_left = middle_x, middle_y
        elif (top < middle_x) and (left >= middle_y):  # top-right corner
            new_top, new_left = middle_x, 0
        elif (top >= middle_x) and (left < middle_y):  # bottom-left corner
            new_top, new_left = 0, middle_y
        elif (top >= middle_x) and (left >= middle_y):  # bottom-right corner
            new_top, new_left = 0, 0

        # crop the pattern
        pattern = crop(obj)

        # calculate the new position on the output grid
        new_x = new_top + (top - middle_x) if top >= middle_x else new_top + top
        new_y = new_left + (left - middle_y) if left >= middle_y else new_left + left

        # place the pattern on the new position
        blit_sprite(output_grid, pattern, new_x, new_y, background=Color.BLACK)

        # clear the old position
        for i in range(top, top + width):
            for j in range(left, left + height):
                output_grid[i, j] = Color.BLACK

    return output_grid

def generate_input():
    # make a grid of random size with black background
    n = m = np.random.randint(10, 15)
    grid = np.full((n, m), Color.BLACK)

    # fill the grid with random block-like pattern of random colors
    num_patterns = np.random.randint(1, 5)
    for _ in range(num_patterns):
        block_size = np.random.randint(2, 6)
        colors = np.random.choice(list(Color.NOT_BLACK), 4, replace=False)
        block = np.array([[np.random.choice(colors) for _ in range(block_size)] for _ in range(block_size)])

        # place the block in one of the four corners
        corner_x, corner_y = np.random.randint(0, 2), np.random.randint(0, 2)
        start_x = corner_x * (n // 2)
        start_y = corner_y * (m // 2)

        # Check if the block fits in the chosen corner
        if start_x + block_size <= n and start_y + block_size <= m:
            blit_sprite(grid, block, start_x, start_y, background=Color.BLACK)

    return grid