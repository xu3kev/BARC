from common import *

import numpy as np
from typing import *


# concepts:
# sliding objects, patterns

# description:
# In the input grid, there is a horizontal bar of colored pixels (the sliding object) located somewhere in the grid.
# To produce the output grid, extend lines downwards from each pixel in the bar until they reach a specified termination pattern located somewhere below it in the grid.
# The colors of the lines will match the colors of the pixels in the bar.

def main(input_grid):

    # Get dimensions of the input grid
    n, m = input_grid.shape

    # Determine bar position by finding the first non-black row
    bar_y = next(y for y in range(n) if np.any(input_grid[y] != Color.BLACK))

    # Determine termination pattern position by finding first row of pattern
    pattern_y = next(y for y in range(bar_y + 1, n) if np.any(input_grid[y] != Color.BLACK))

    # Create output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through pixels in the bar
    for x in range(m):
        if input_grid[bar_y, x] != Color.BLACK:
            color = input_grid[bar_y, x]
            # Draw vertical line until termination pattern is encountered
            for y in range(bar_y + 1, pattern_y):
                if input_grid[y, x] != Color.BLACK:
                    break
                output_grid[y, x] = color

    return output_grid


def generate_input():
    # Create a 10x10 black grid
    input_grid = np.full((10, 10), Color.BLACK)

    # Choose random colors for the bar and the termination pattern
    bar_color = np.random.choice(list(Color.NOT_BLACK))
    pattern_colors = np.random.choice(Color.NOT_BLACK, 2, replace=False)

    # Insert a horizontal bar at a random row
    bar_y = np.random.randint(0, 5)
    for x in range(10):
        if np.random.rand() < 0.5:
            input_grid[bar_y, x] = bar_color

    # Insert a termination pattern at a row below the bar
    pattern_y = np.random.randint(bar_y + 1, 9)
    for x in range(10):
        if np.random.rand() < 0.5:
            input_grid[pattern_y, x] = np.random.choice(pattern_colors)

    return input_grid