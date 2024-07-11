from common import *

import numpy as np
from typing import *

# concepts:
# vertical lines, growing, alignment

# description:
# In the input you will see individual pixels sprinkled on a black background that are either red, green, or blue.
# Turn each colored pixel into a vertical bar that grows upwards until it reaches the top of the grid or another colored pixel.
# The bars should be ordered from left to right: red bars first, then green bars, then blue bars.
# If multiple bars of the same color would overlap, only keep the leftmost one.

def main(input_grid):
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Extract colored pixels
    red_pixels = np.argwhere(input_grid == Color.RED)
    green_pixels = np.argwhere(input_grid == Color.GREEN)
    blue_pixels = np.argwhere(input_grid == Color.BLUE)

    # Sort pixels by x-coordinate (leftmost first)
    red_pixels = sorted(red_pixels, key=lambda x: x[1])
    green_pixels = sorted(green_pixels, key=lambda x: x[1])
    blue_pixels = sorted(blue_pixels, key=lambda x: x[1])

    # Function to grow a bar upwards
    def grow_bar(x, y, color):
        for i in range(y, -1, -1):
            if output_grid[i, x] != Color.BLACK:
                break
            output_grid[i, x] = color

    # Process red pixels
    for x, y in red_pixels:
        if output_grid[y, x] == Color.BLACK:
            grow_bar(x, y, Color.RED)

    # Process green pixels
    for x, y in green_pixels:
        if output_grid[y, x] == Color.BLACK:
            grow_bar(x, y, Color.GREEN)

    # Process blue pixels
    for x, y in blue_pixels:
        if output_grid[y, x] == Color.BLACK:
            grow_bar(x, y, Color.BLUE)

    return output_grid

def generate_input():
    # Make a black grid of random size
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # Sprinkle some red, green, and blue pixels
    num_pixels = np.random.randint(5, 15)
    for _ in range(num_pixels):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        color = np.random.choice([Color.RED, Color.GREEN, Color.BLUE])
        grid[x, y] = color

    return grid