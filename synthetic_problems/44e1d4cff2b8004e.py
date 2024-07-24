from common import *

import numpy as np
from typing import *

# concepts:
# reflection, cropping

# description:
# In the input, you will see a square pattern of random colors except black.
# To make the output, reflect the pattern vertically and then crop the black borders around the reflected pattern.

def main(input_grid: np.ndarray) -> np.ndarray:
    # take the input pattern
    pattern = input_grid

    # reflect the pattern vertically
    reflected_pattern = pattern[::-1, :]

    # combine the original and reflected patterns
    combined_pattern = np.concatenate((pattern, reflected_pattern), axis=0)

    # crop the black borders out of the combined pattern
    output_grid = crop(combined_pattern, background=Color.BLACK)

    return output_grid

def generate_input() -> np.ndarray:
    n = np.random.randint(8,12)  # height/width of the grid
    grid = np.full((n, n), Color.BLACK, dtype=int)

    # create a random square pattern of size (n//2)x(n) with random colors except black
    pattern_height = n // 2
    pattern = random_sprite(pattern_height, n, density=1, symmetry="not_symmetric", color_palette=Color.NOT_BLACK)

    # blit the pattern onto the upper half of the grid
    grid[:pattern_height, :] = pattern

    return grid