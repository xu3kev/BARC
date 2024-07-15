from common import *

import numpy as np
from typing import *


# concepts:
# counting, incrementing, horizontal bars, patterns

# description:
# In the input, you will see a row partially filled with pixels of one color from the left.
# To make the output: 
# 1. Copy the partially filled row horizontally.
# 2. Each row increases the count of colored pixels from the previous row by one.
# 3. Each new row is mirrored horizontally.
# 4. Repeat until you fill the grid vertically.


def main(input_grid):
    # Get the size of the input grid
    input_height, input_width = input_grid.shape

    # Determine the color used for the horizontal bar
    unique_colors = set(input_grid[input_grid != Color.BLACK])
    if len(unique_colors) != 1:
        raise ValueError("The input grid must have exactly one unique non-black color.")
    color = unique_colors.pop()

    # Create an empty output grid of 10 rows by 10 columns
    output_height = 10
    output_width = 10
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Generate the increasing horizontal bars with mirroring
    for i in range(output_height):
        # Calculate number of colored pixels
        num_colored_pixels = min(i + 1, output_width // 2)  # Half as maximum before mirroring

        # Create the bar with spacing for mirroring
        bar = [color] * num_colored_pixels + [Color.BLACK] * (output_width - 2 * num_colored_pixels) + [color] * num_colored_pixels

        # Place the bar in the corresponding row
        output_grid[i] = bar

    return output_grid


def generate_input():
    # Create an empty 1x10 grid
    input_grid = np.zeros((1, 10), dtype=int)

    # Decide the color to partially fill the row
    color = np.random.choice(list(Color.NOT_BLACK))

    # Randomly choose how many pixels to fill initially
    num_colored_pixels = np.random.randint(1, 6)

    # Fill the row with the chosen color
    input_grid[0, :num_colored_pixels] = color

    return input_grid

# Example usage