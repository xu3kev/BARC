from common import *

import numpy as np
from typing import *

# concepts:
# pattern copying, translation

# description:
# In the input, you will see a small grid with a pattern of random colors except black.
# To make the output, paste the pattern multiple times to create a tiling effect based on specified intervals.

def main(input_grid):
    # take the input pattern
    pattern = input_grid

    pattern_height, pattern_width = pattern.shape
    pattern_interval = 2  # specify interval for tiling

    # make the output grid to fit multiples of the pattern
    output_height = pattern_interval * pattern_height
    output_width = pattern_interval * pattern_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # paste the pattern in the output grid with specified intervals
    for i in range(output_height // pattern_height):
        for j in range(output_width // pattern_width):
            start_x = i * pattern_height * pattern_interval
            start_y = j * pattern_width * pattern_interval
            blit(output_grid, pattern, start_x, start_y)

    return output_grid

def generate_input():
    # make a random square pattern of random size and colors
    n = m = np.random.randint(2, 4)
    pattern = random_sprite(n, m, density=1, symmetry="not_symmetric", color_palette=Color.NOT_BLACK)

    return pattern