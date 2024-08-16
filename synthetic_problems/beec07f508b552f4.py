from common import *

import numpy as np
from typing import *

# concepts:
# repetition, patterns, positioning, mirroring

# description:
# Given an input grid, find the pattern located in the top-left corner of the grid.
# Mirror that pattern diagonally across the grid, repeating until the grid is filled.
# The output grid should be of the same size as the input grid.

def main(input_grid):
    # Find the smallest bounding box of the top-left pattern.
    objects = find_connected_components(input_grid, connectivity=8)
    top_left_object = objects[0]
    top_left_x, top_left_y, obj_w, obj_h = bounding_box(top_left_object)

    # Crop the top-left pattern to use as a template pattern
    pattern = crop(top_left_object)

    # Initialize the output grid with the same size as input grid
    output_grid = np.copy(input_grid)

    # Get the shape of the input grid
    n, m = input_grid.shape

    # Place the pattern diagonally across the grid until it is filled
    pattern_w, pattern_h = pattern.shape
    for i in range(0, n, pattern_h):
        for j in range(0, m, pattern_w):
            blit_sprite(output_grid, pattern, i, j, background=Color.BLACK)

    return output_grid


def generate_input():
    # Random size of the input grid
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)

    # Initialize the grid with a black background
    grid = np.full((n, m), Color.BLACK)

    # Define the size of the pattern to be placed in the top-left corner
    pattern_size = np.random.randint(2, 5)
    pattern_color = np.random.choice(list(Color.NOT_BLACK))

    # Create the pattern in the top-left corner
    grid[:pattern_size, :pattern_size] = [[np.random.choice([pattern_color, Color.BLACK]) for _ in range(pattern_size)] for _ in range(pattern_size)]

    return grid