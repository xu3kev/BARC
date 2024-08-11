from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines, color, rectangular cells

# description:
# In the input, you will see multiple distinct colored pixels randomly placed inside a rectangular grid on a black background.
# To make the output, for each colored pixel, draw two diagonal lines of the same color starting from the position of each pixel such that they form an `X` shape, intersecting at the pixel's location.

def main(input_grid):
    output_grid = np.copy(input_grid)

    # Find the positions of all the colored pixels that are not black
    colored_pixels = []
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != Color.BLACK:
                colored_pixels.append((i, j, input_grid[i, j]))

    # For each colored pixel, draw two diagonals forming an `X`
    for x, y, color in colored_pixels:
        # Draw diagonals
        # first diagonal
        draw_line(output_grid, x, y, length=None, color=color, direction=(1, -1))
        draw_line(output_grid, x, y, length=None, color=color, direction=(-1, 1))
        # second diagonal
        draw_line(output_grid, x, y, length=None, color=color, direction=(-1, -1))
        draw_line(output_grid, x, y, length=None, color=color, direction=(1, 1))

    return output_grid

def generate_input():
    # Create a grid of random dimensions
    n = m = np.random.randint(5, 20)
    grid = np.full((n, m), Color.BLACK, dtype=int)

    # Fill random positions with distinct colors
    num_colored_pixels = np.random.randint(1, min(n, m))
    colored_positions = random.sample([(i, j) for i in range(n) for j in range(m)], num_colored_pixels)
    colors = random.sample(Color.NOT_BLACK, num_colored_pixels)

    for (x, y), color in zip(colored_positions, colors):
        grid[x, y] = color

    return grid