from common import *

import numpy as np
from typing import *

# concepts:
# vertical lines, growing, repetition, counting

# description:
# In the input, you will see individual pixels sprinkled on a black background that are either red, green, or blue.
# For each red pixel, create a vertical bar that extends upwards until it hits another colored pixel or the edge of the grid.
# For each green pixel, create a horizontal bar that extends to the right until it hits another colored pixel or the edge of the grid.
# For each blue pixel, count the number of red and green pixels in its row and column (excluding itself).
# Replace the blue pixel with that many blue pixels in a vertical line extending downwards.

def main(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Process red pixels (vertical bars extending upwards)
    red_pixels = np.argwhere(input_grid == Color.RED)
    for x, y in red_pixels:
        for i in range(x, -1, -1):  # Move upwards
            if output_grid[i, y] == Color.BLACK:
                output_grid[i, y] = Color.RED
            else:
                break  # Stop if we hit a non-black pixel

    # Process green pixels (horizontal bars extending right)
    green_pixels = np.argwhere(input_grid == Color.GREEN)
    for x, y in green_pixels:
        for j in range(y, input_grid.shape[1]):  # Move right
            if output_grid[x, j] == Color.BLACK:
                output_grid[x, j] = Color.GREEN
            else:
                break  # Stop if we hit a non-black pixel

    # Process blue pixels
    blue_pixels = np.argwhere(input_grid == Color.BLUE)
    for x, y in blue_pixels:
        # Count red and green pixels in the same row and column
        count = np.sum((input_grid[x, :] == Color.RED) | (input_grid[x, :] == Color.GREEN)) + \
                np.sum((input_grid[:, y] == Color.RED) | (input_grid[:, y] == Color.GREEN)) - \
                ((input_grid[x, y] == Color.RED) | (input_grid[x, y] == Color.GREEN))  # Avoid double-counting
        
        # Replace blue pixel with vertical line of blue pixels
        for i in range(x, min(x + count, input_grid.shape[0])):
            output_grid[i, y] = Color.BLUE

    return output_grid

def generate_input():
    # Create a black grid of random size
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # Sprinkle red, green, and blue pixels
    for color in [Color.RED, Color.GREEN, Color.BLUE]:
        num_pixels = np.random.randint(1, 5)
        for _ in range(num_pixels):
            x, y = np.random.randint(0, n), np.random.randint(0, m)
            while grid[x, y] != Color.BLACK:  # Ensure we don't overwrite existing colored pixels
                x, y = np.random.randint(0, n), np.random.randint(0, m)
            grid[x, y] = color

    return grid