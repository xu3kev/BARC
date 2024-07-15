import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, bitmasks with separator, direction, lines

# description:
# The input grid consists of two bitmasks separated by a grey vertical bar. 
# The left bitmask uses blue pixels, while the right bitmask uses red pixels.
# To produce the output:
# 1. Perform a logical XOR operation between the two bitmasks.
# 2. For each resulting 'true' pixel, draw a line in the direction specified by that pixel's position:
#    - If it's in the top-left quadrant, draw a line towards the top-left corner
#    - If it's in the top-right quadrant, draw a line towards the top-right corner
#    - If it's in the bottom-left quadrant, draw a line towards the bottom-left corner
#    - If it's in the bottom-right quadrant, draw a line towards the bottom-right corner
# The lines should be drawn in yellow and should extend until they reach the edge of the grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the grey vertical bar
    for x_bar in range(input_grid.shape[1]):
        if np.all(input_grid[:, x_bar] == Color.GREY):
            break

    left_mask = input_grid[:, :x_bar]
    right_mask = input_grid[:, x_bar+1:]

    # Perform XOR operation
    xor_result = np.logical_xor(left_mask == Color.BLUE, right_mask == Color.RED)

    # Create output grid
    output_grid = np.full(left_mask.shape, Color.BLACK)

    # Find center of the grid
    center_y, center_x = np.array(output_grid.shape) // 2

    # Draw lines for each 'true' pixel in XOR result
    for y, x in np.argwhere(xor_result):
        if y < center_y:
            if x < center_x:
                direction = (-1, -1)  # top-left
            else:
                direction = (-1, 1)   # top-right
        else:
            if x < center_x:
                direction = (1, -1)   # bottom-left
            else:
                direction = (1, 1)    # bottom-right
        
        draw_line(output_grid, x, y, length=None, color=Color.YELLOW, direction=direction)

    return output_grid

def generate_input() -> np.ndarray:
    # Create a pair of equally sized bitmasks
    width, height = np.random.randint(10, 20), np.random.randint(10, 20)

    grid1 = np.random.choice([Color.BLUE, Color.BLACK], size=(height, width))
    grid2 = np.random.choice([Color.RED, Color.BLACK], size=(height, width))
    
    # Create a grey vertical bar
    bar = np.full((height, 1), Color.GREY)

    # Combine the grids
    grid = np.hstack((grid1, bar, grid2))

    return grid