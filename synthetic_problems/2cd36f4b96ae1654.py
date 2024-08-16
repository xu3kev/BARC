from common import *

import numpy as np
from typing import *

# concepts:
# Reflection, Pixel manipulation, Color guide, Rotation

# description:
# In the input, you will see a distinct colored square in the center of the grid.
# The transformation involves rotating the grid by 90 degrees clockwise around the square.
# The output should be the rotated grid while maintaining the square's position and size.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    middle_square_size = 3  # it's a 3x3 square in the center

    # Find the center of the grid
    center_x, center_y = n // 2, m // 2

    # Extract the center square
    center_square = input_grid[center_x-1:center_x+2, center_y-1:center_y+2]

    # Rotate the entire grid by 90 degrees clockwise
    rotated_grid = np.rot90(input_grid, k=-1)

    # Embed the center square back into the rotated grid
    rotated_grid[center_x-1:center_x+2, center_y-1:center_y+2] = center_square

    return rotated_grid

def generate_input():
    n, m = np.random.randint(10, 20, size=2)
    grid = np.random.choice(list(Color.NOT_BLACK), (n, m))
    center_x, center_y = n // 2, m // 2

    # Create a distinct colored square in the center
    square_color = np.random.choice(Color.NOT_BLACK)
    grid[center_x-1:center_x+2, center_y-1:center_y+2] = square_color

    return grid