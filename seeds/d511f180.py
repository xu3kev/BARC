from common import *

import numpy as np
from typing import *

# concepts:
# colors

# description:
# To create the output grid, swap the teal and grey colors in the grid.

def main(input_grid):
    output_grid = input_grid.copy()
    output_grid[input_grid == Color.GREY] = Color.TEAL
    output_grid[input_grid == Color.TEAL] = Color.GREY
    return output_grid


def generate_input():
    # make a random grid
    n = np.random.randint(3, 10)
    input_grid = np.random.choice(Color.NOT_BLACK, size=(n, n))
    return input_grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
