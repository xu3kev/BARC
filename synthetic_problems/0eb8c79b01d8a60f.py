from common import *

import numpy as np

# concepts:
# symmetry, objects, reflection

# description:
# In the input, you will see a square pattern of random colors except black.
# To make the output, reflect the pattern both vertically and horizontally, resulting in four quadrants of the original pattern to form a larger grid with full symmetry.

def main(input_grid):
    # take the input pattern
    pattern = input_grid

    # reflect the pattern vertically
    vertically_reflected = pattern[:, ::-1]

    # reflect the pattern horizontally
    horizontally_reflected = pattern[::-1, :]

    # reflect the pattern both vertically and horizontally
    both_reflected = pattern[::-1, ::-1]

    # create the output grid by combining the quadrants
    top_half = np.concatenate((pattern, vertically_reflected), axis=1)
    bottom_half = np.concatenate((horizontally_reflected, both_reflected), axis=1)
    output_grid = np.concatenate((top_half, bottom_half), axis=0)

    return output_grid

def generate_input():
    # make a random square pattern of random size and colors
    n = m = np.random.randint(3, 6)
    grid = random_sprite(n, m, density=1, symmetry="not_symmetric", color_palette=Color.NOT_BLACK)

    return grid