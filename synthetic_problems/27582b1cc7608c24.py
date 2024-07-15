from common import *

import numpy as np
from typing import *

# concepts:
# patterns, copying, positioning, rotation

# description:
# In the input, you will see a pattern of pixels in the top left corner of the grid. The pattern is enclosed in a rectangular region with all pixels the same color (not black).
# To make the output, copy the pattern to each of the four corners of the grid, rotating each pattern to match the corner's orientation. The output grid will be twice the size of the input grid, minus one pixel in each dimension.

def main(input_grid):
    # get the patterns from the input
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=False)

    # sort the objects by their size to find the pattern, assuming the largest object is the enclosing rectangle
    sorted_objects = sorted(objects, key=lambda x: -np.count_nonzero(x))
    pattern_object = sorted_objects[0]

    # find the bounding box of the pattern
    x, y, width, height = bounding_box(pattern_object)

    # extract the pattern
    pattern = input_grid[x:x+width, y:y+height]

    # create the output grid, twice the size of the input grid minus one pixel in each dimension
    output_grid = np.full((input_grid.shape[0] * 2 - 1, input_grid.shape[1] * 2 - 1), Color.BLACK)

    # place the pattern in each corner, rotating appropriately
    corners = [(0, 0), (0, output_grid.shape[1] - height), (output_grid.shape[0] - width, 0), (output_grid.shape[0] - width, output_grid.shape[1] - height)]
    rotations = [0, 1, 3, 2]  # rotations required (0Â° for top left, 90Â° for top right, 270Â° for bottom left, 180Â° for bottom right)

    for (cx, cy), rotation in zip(corners, rotations):
        rotated_pattern = np.rot90(pattern, k=rotation)
        blit_sprite(output_grid, rotated_pattern, cx, cy, background=Color.BLACK)

    return output_grid
    

def generate_input():
    # make a random sized grid with black background
    n = np.random.randint(5, 8)
    m = np.random.randint(5, 8)
    grid = np.zeros((n, m), dtype=int)

    # select a color for the pattern
    color = np.random.choice(list(Color.NOT_BLACK))

    # select a size for the pattern so that there will be space for the enclosing rectangle
    width = np.random.randint(2, (m - 2))
    height = np.random.randint(2, (n - 2))

    # create an enclosing rectangle with the chosen color
    grid[0:height, 0:width] = color

    # scatter random black pixels within the enclosing rectangle to form the pattern
    num_patterns = np.random.randint(1, height * width // 2)
    for _ in range(num_patterns):
        x, y = np.random.randint(0, width), np.random.randint(0, height)
        grid[y, x] = Color.BLACK

    return grid