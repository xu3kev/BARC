from common import *

import numpy as np
from typing import *

# concepts:
# positioning, copying, reflection

# description:
# In the input, you will see a pattern of pixels in the four quadrants of a square grid. All the pixels are the same color, and the patterns are square regions.
# To make the output, rotate the pattern in the first quadrant 90 degrees clockwise, the pattern in the second quadrant 90 degrees counter-clockwise, the pattern in the third quadrant 180 degrees, and leave the pattern in the fourth quadrant as-is.

def rotate_pattern(pattern, angle):
    """ Rotate pattern by the given angle """
    if angle == 90:
        return np.rot90(pattern, -1)  # Counter-clockwise by default, so -1 means clockwise
    elif angle == -90:
        return np.rot90(pattern, 1)  # 90 degrees counter-clockwise
    elif angle == 180:
        return np.rot90(pattern, 2)  # 180 degrees
    return pattern  # 0 degrees, do nothing

def main(input_grid):
    # Dimensions of the grid
    n, m = input_grid.shape

    # Ensure the grid is square
    assert n == m, "Grid is not square!"

    # Determine the size of each quadrant, assuming it's square
    quadrant_size = n // 2

    # Extract the 4 quadrants
    top_left = input_grid[:quadrant_size, :quadrant_size]
    top_right = input_grid[:quadrant_size, quadrant_size:]
    bottom_left = input_grid[quadrant_size:, :quadrant_size]
    bottom_right = input_grid[quadrant_size:, quadrant_size:]

    # Rotate each quadrant accordingly
    top_left_rotated = rotate_pattern(top_left, 90)
    top_right_rotated = rotate_pattern(top_right, -90)
    bottom_left_rotated = rotate_pattern(bottom_left, 180)
    bottom_right_rotated = rotate_pattern(bottom_right, 0)

    # Create the output grid
    output_grid = np.zeros_like(input_grid)

    # Place rotated patterns back in their quadrants
    output_grid[:quadrant_size, :quadrant_size] = top_left_rotated
    output_grid[:quadrant_size, quadrant_size:] = top_right_rotated
    output_grid[quadrant_size:, :quadrant_size] = bottom_left_rotated
    output_grid[quadrant_size:, quadrant_size:] = bottom_right_rotated

    return output_grid


def generate_input():
    # make a random sized square grid with black background
    n = np.random.randint(8, 12)
    grid = np.zeros((n, n), dtype=int)

    # select a color for the patterns
    color = np.random.choice(list(Color.NOT_BLACK))

    # select a size for the patterns so that there will be space between the patterns after they are placed in their quadrants
    quadrant_size = n // 2

    # make a random pattern in each quadrant using the selected size
    for i in range(2):
        for j in range(2):
            pattern_size = np.random.randint(2, quadrant_size + 1)
            pattern = [[np.random.choice([color, Color.BLACK]) for _ in range(pattern_size)] for _ in range(pattern_size)]
            x_start = i * quadrant_size
            y_start = j * quadrant_size
            grid[x_start:x_start+pattern_size, y_start:y_start+pattern_size] = pattern

    return grid