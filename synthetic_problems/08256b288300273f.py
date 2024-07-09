from common import *

import numpy as np
from typing import *

# concepts:
# growing, symmetry, horizontal/vertical bars

# description:
# In the input, you will see individual pixels sprinkled on a black background that are either red, green, or blue.
# For each colored pixel:
# - If it's red, grow it into a square with the original pixel at its center.
# - If it's green, grow it into a horizontal bar with the original pixel at its center.
# - If it's blue, grow it into a vertical bar with the original pixel at its center.
# All grown shapes should be symmetrical around their original pixel.
# If shapes overlap, the order of precedence is red > green > blue.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Process blue pixels first (lowest precedence)
    blue_pixels = np.argwhere(input_grid == Color.BLUE)
    for x, y in blue_pixels:
        output_grid[:, y] = Color.BLUE

    # Process green pixels next
    green_pixels = np.argwhere(input_grid == Color.GREEN)
    for x, y in green_pixels:
        output_grid[x, :] = Color.GREEN

    # Process red pixels last (highest precedence)
    red_pixels = np.argwhere(input_grid == Color.RED)
    for x, y in red_pixels:
        # Determine the size of the square (random, but deterministic based on position)
        size = ((x + y) % 3) + 3  # This will give a size between 3 and 5
        half_size = size // 2
        
        # Calculate the boundaries of the square
        x_min = max(0, x - half_size)
        x_max = min(n, x + half_size + 1)
        y_min = max(0, y - half_size)
        y_max = min(m, y + half_size + 1)
        
        # Draw the red square
        output_grid[x_min:x_max, y_min:y_max] = Color.RED

    return output_grid

def generate_input():
    # Make a black grid of random size
    n, m = np.random.randint(15, 25), np.random.randint(15, 25)
    grid = np.zeros((n, m), dtype=int)

    # Sprinkle some red, green, and blue pixels
    num_pixels = np.random.randint(5, 15)
    for _ in range(num_pixels):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        color = random.choice([Color.RED, Color.GREEN, Color.BLUE])
        grid[x, y] = color

    return grid