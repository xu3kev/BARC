from common import *

import numpy as np
from typing import *

# concepts:
# counting, resizing, objects, color, alignment

# description:
# In the input, you see a grid with a row of colored blocks at the bottom and the right.
# There's also a "T"-shaped pattern in the top-left that is not touching the other colors.
# To create the output:
# 1. count the number of unique colors that aren't black
# 2. enlarge every pixel in the input by a factor of the square root of the number of unique colors (round down)
# 3. ensure the "T"-pattern in the top-left remains proportional and connected after transformation.

def main(input_grid):
    # count the number of unique colors that aren't black
    unique_colors = len(set(input_grid.flatten())) - 1

    # calculate the enlargement factor
    factor = int(np.sqrt(unique_colors))

    # magnify the pixels
    output_grid = np.repeat(np.repeat(input_grid, factor, axis=0), factor, axis=1)

    return output_grid

def generate_input():
    # make a 6x6 black grid for the background
    n = m = 6
    grid = np.zeros((n, m), dtype=int)

    # generate the "T"-shape at the top-left
    t_color = np.random.choice(list(Color.NOT_BLACK))
    grid[0, 1:4] = t_color
    grid[1:4, 2] = t_color

    # pick the remaining colors
    remaining_colors = list(set(Color.NOT_BLACK) - {t_color})

    # create a sequence of colors for the bottom and right of the grid
    sequence = []
    while len(sequence) < 6:
        color = np.random.choice(remaining_colors)
        remaining_colors.remove(color)
        length = np.random.randint(1, 6 - len(sequence) + 1)
        sequence.extend([color] * length)

    # ensure sequence is the same for the bottom row and the right column
    bottom_sequence = sequence[:6]
    grid[-1, :] = bottom_sequence
    grid[:, -1] = bottom_sequence

    return grid