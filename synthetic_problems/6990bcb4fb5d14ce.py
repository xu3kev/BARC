from common import *

import numpy as np
from typing import *

# concepts:
# patterns, reflection, counting, positioning

# description:
# In the input grid, you will see a row of colored pixels with black pixels filling the rest of the grid.
# To create the output:
# 1. Create a new grid that is double the height of the input grid.
# 2. Copy the input grid to the top half of the new grid.
# 3. Reflect the row of colored pixels along the x-axis (vertical axis) and position the mirrored row at the bottom of the new grid.

def main(input_grid):
    # Get the dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Create an output grid that is double the height of the input grid
    output_grid = np.zeros((input_height * 2, input_width), dtype=int)

    # Copy the input grid to the top half of the new grid
    output_grid[:input_height, :] = input_grid

    # Reflect the input grid along the x-axis and copy it to the bottom half of the new grid
    output_grid[input_height:, :] = input_grid[::-1, :]

    return output_grid

def generate_input():
    # Decide the width of the row
    width = np.random.randint(4, 10)

    # Decide the height of the grid
    height = np.random.randint(1, 3)

    # Create an input grid with black background
    grid = np.zeros((height, width), dtype=int)

    # Decide the color to fill the row with
    color = random.choice(list(Color.NOT_BLACK))

    # Randomly determine the number of colored pixels to fill in the row
    num_colored_pixels = np.random.randint(1, width + 1)

    # Fill the row with colored pixels from left to right
    grid[0, :num_colored_pixels] = color

    return grid