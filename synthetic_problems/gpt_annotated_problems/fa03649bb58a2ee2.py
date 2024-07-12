from common import *

import numpy as np
from typing import *

# concepts:
# repeating patterns, colors as indicators, scaling, rotation

# description:
# In the input you will see a nxn sprite with a black background. 
# Construct an output grid with 4n x 4n black pixels. Divide the output grid into 4x4 subgrids.
# For each subgrid, look at the corresponding pixel in the nxn input grid. If the corresponding pixel is not black,
# then copy the nxn input grid into the subgrid, rotating it based on the color:
# - Red: No rotation
# - Blue: 90 degrees clockwise
# - Green: 180 degrees
# - Yellow: 270 degrees clockwise
# If the corresponding pixel is black, the subgrid remains black.

def main(input_grid):
    n = input_grid.shape[0]
    output_grid = np.zeros((4*n, 4*n), dtype=int)

    for i in range(n):
        for j in range(n):
            if input_grid[i, j] != Color.BLACK:
                subgrid = np.rot90(input_grid, k=get_rotation(input_grid[i, j]))
                blit_sprite(output_grid, subgrid, 4*i, 4*j)
    
    return output_grid

def get_rotation(color):
    if color == Color.RED:
        return 0
    elif color == Color.BLUE:
        return 3  # 90 degrees clockwise
    elif color == Color.GREEN:
        return 2  # 180 degrees
    elif color == Color.YELLOW:
        return 1  # 270 degrees clockwise
    else:
        return 0  # Default: no rotation

def generate_input():
    n = random.randint(3, 6)
    color_palette = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
    return random_sprite(n, n, color_palette=color_palette)