from common import *

import numpy as np
from typing import *


# concepts:
# patterns

# description:
# In the input you will see a 3x3 grid made up of black pixels and random non-black color pixels.
# Ignore the non-black pixels, return single pixel of a color that is dependent on the pattern made by the black pixels.

def main(input_grid):
    # we have four possible patterns that the black pixels can form that correspond to a specific color as follows:
    blue = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 1]]).T
    red = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]).T
    green = np.array([[1, 0, 0], [1, 0, 0], [0, 1, 1]]).T
    pink = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]]).T

    # now we want to mask the input grid to have a 1 where the black pixels are and a 0 where the non-black pixels are
    mask = (input_grid == Color.BLACK).astype(int)

    # now we want to check which pattern the black pixels form and return the corresponding color
    if np.array_equal(mask, blue):
        return np.full((1, 1), Color.BLUE)
    elif np.array_equal(mask, red):
        return np.full((1, 1), Color.RED)
    elif np.array_equal(mask, green):
        return np.full((1, 1), Color.GREEN)
    elif np.array_equal(mask, pink):
        return np.full((1, 1), Color.PINK)
    
    # if the black pixels do not form any of the patterns, assert False
    assert False


def generate_input():
    # first create a 3x3 grid full of a random color (not black)
    grid = np.full((3, 3), new_random_color())

    # now we want to randomly choose one of the four patterns and place it in the grid
    blue = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 1]]).T
    red = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]).T
    green = np.array([[1, 0, 0], [1, 0, 0], [0, 1, 1]]).T
    pink = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]]).T
    pattern = random.choice([blue, red, green, pink])
    grid = np.where(pattern == 1, Color.BLACK, grid)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)