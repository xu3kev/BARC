from common import *

import numpy as np
from typing import *


def main(input_grid):
    n, m = input_grid.shape

    output_grid = np.copy(input_grid)

    for i in range(n):
        for j in range(m // 2):
            mirror_j = m - j - 1
            # Using the same color on the right half to make it symmetric
            output_grid[i, mirror_j] = input_grid[i, j]

    return output_grid


def generate_input():
    n = np.random.randint(5, 8)
    m = n * 2  # making the grid wider to accommodate mirror symmetry
    grid = np.zeros((n, m), dtype=int)

    # Fill the left half with random colors
    for i in range(n):
        for j in range(m // 2):
            grid[i, j] = np.random.choice(list(Color.NOT_BLACK))

    return grid