from common import *

import numpy as np
from typing import *

# concepts:
# objects, object splitting, object transformation

# description:
# The input consists of a grid with a single contiguous object in the middle of the grid.
# For the output, split the object vertically into two equal halves. Place the left half in the top-left corner and the right half in the bottom-right corner.

def main(input_grid):
    # find the bounding box of the object
    x, y, width, height = bounding_box(input_grid, background=Color.BLACK)

    # crop the object from the grid using the bounding box
    object = input_grid[y:y+height, x:x+width]

    # split the object vertically into two equal halves
    left_half = object[:, :width // 2]
    right_half = object[:, width // 2:]

    # create the output grid
    output_grid = np.zeros_like(input_grid, dtype=int)

    # place the left half in the top-left corner
    blit(output_grid, left_half)

    # place the right half in the bottom-right corner
    blit(output_grid, right_half, x=output_grid.shape[1] - right_half.shape[1], y=output_grid.shape[0] - right_half.shape[0])

    return output_grid

def generate_input():
    # create a black grid
    n = 10
    grid = np.zeros((n, n), dtype=int)

    # select a color for the object
    object_color = np.random.choice(list(Color.NOT_BLACK))

    # make a random sprite of size (approximately) half the grid to ensure it fits comfortably
    sprite = random_sprite(n // 2, n // 2, color_palette=[object_color], symmetry='not_symmetric')

    # place the sprite in the middle of the grid
    start_x = (grid.shape[1] - sprite.shape[1]) // 2
    start_y = (grid.shape[0] - sprite.shape[0]) // 2
    blit(grid, sprite, x=start_x, y=start_y)

    return grid