from common import *

import numpy as np
from typing import *

# concepts:
# repeating patterns, scaling, symmetry, colors as indicators

# description:
# In the input, you will see a nxn sprite with a black background and colored pixels.
# Construct an output grid with 3n x 3n black pixels. Divide the output grid into 3x3 subgrids.
# For each subgrid, look at the corresponding pixel in the nxn input grid:
# - If the pixel is black, leave the subgrid black.
# - If the pixel is colored, copy a rotated version of the input grid into the subgrid:
#   - For red pixels, rotate 90 degrees clockwise
#   - For blue pixels, rotate 180 degrees
#   - For green pixels, rotate 270 degrees clockwise
#   - For any other color, don't rotate (0 degrees)

def main(input_grid):
    n = input_grid.shape[0]
    output_grid = np.zeros((3*n, 3*n), dtype=int)

    for i in range(n):
        for j in range(n):
            if input_grid[i, j] != Color.BLACK:
                subgrid = np.copy(input_grid)
                
                # Rotate based on color
                if input_grid[i, j] == Color.RED:
                    subgrid = np.rot90(subgrid, k=3)  # 90 degrees clockwise
                elif input_grid[i, j] == Color.BLUE:
                    subgrid = np.rot90(subgrid, k=2)  # 180 degrees
                elif input_grid[i, j] == Color.GREEN:
                    subgrid = np.rot90(subgrid, k=1)  # 270 degrees clockwise
                # For any other color, no rotation (0 degrees)
                
                # Copy the rotated subgrid into the output grid
                output_grid[3*i:3*i+n, 3*j:3*j+n] = subgrid

    return output_grid

def generate_input():
    n = random.randint(3, 6)
    color_palette = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.GREY, Color.PINK, Color.ORANGE, Color.TEAL, Color.MAROON]
    return random_sprite(n, n, color_palette=color_palette, density=0.3)