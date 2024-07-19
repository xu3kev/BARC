from common import *

import numpy as np
from typing import *


# concepts:
# cropping, patterns, coloring diagonal pixels

# description:
# In the input you will see a grid with randomly colored pixels on a black background.
# To make the output, crop the input grid to the bounding box containing all non-black pixels.
# Then, for each pixel in the cropped grid that's not black, color the diagonal pixels surrounding it a consistent color (TEAL) if those diagonal pixels are black.

def main(input_grid):
    # Crop the grid to the smallest bounding box that contains all non-black pixels
    cropped_grid = crop(input_grid, background=Color.BLACK)

    # Create a copy of cropped grid to modify
    output_grid = np.copy(cropped_grid)

    # Define diagonal directions
    diagonal_directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    # Color diagonal pixels around non-black pixels in the cropped grid
    for x in range(cropped_grid.shape[0]):
        for y in range(cropped_grid.shape[1]):
            if cropped_grid[x, y] != Color.BLACK:
                for dx, dy in diagonal_directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < cropped_grid.shape[0] and 0 <= ny < cropped_grid.shape[1] and cropped_grid[nx, ny] == Color.BLACK:
                        output_grid[nx, ny] = Color.TEAL

    return output_grid


def generate_input():
    # Create a grid of size 10x10 to 15x15 with black background
    n, m = np.random.randint(10, 16), np.random.randint(10, 16)
    grid = np.full((n, m), Color.BLACK, dtype=int)

    # Place pixels of random colors (other than black) at random positions 
    num_colored_pixels = np.random.randint(5, 11)
    for _ in range(num_colored_pixels):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        color = np.random.choice(list(Color.NOT_BLACK))
        grid[x, y] = color

    return grid