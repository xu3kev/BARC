from common import *

import numpy as np
from typing import *

# concepts:
# reflection

# description:
# In the input you will see a square pattern of random colors except black.
# To make the output, reflect the pattern vertically, and put the reflected pattern beneath the input pattern.

def main(input_grid):
    # take the input pattern
    pattern = input_grid

    # reflect the pattern vertically
    reflected_pattern = pattern[:, ::-1]

    # make the output grid
    output_grid = np.concatenate((pattern, reflected_pattern), axis=1)

    return output_grid

def generate_input():
    # make a random square pattern of random size and colors
    n = m = np.random.randint(3, 6)
    grid = random_sprite(n, m, density=1, symmetry="not_symmetric", color_palette=Color.NOT_BLACK)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)