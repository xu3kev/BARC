import numpy as np
from typing import *
from common import *

# concepts:
# bitmasks with separator, boolean logical operations, rotation

# description:
# In the input you will see two bitmasks separated by a yellow horizontal bar.
# The top bitmask is in red, and the bottom bitmask is in blue.
# To make the output, perform the following steps:
# 1. Rotate the bottom (blue) bitmask 90 degrees clockwise
# 2. Perform a logical XOR operation between the top (red) bitmask and the rotated bottom bitmask
# 3. Color the resulting pixels green where the XOR operation is true, and black otherwise

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the yellow horizontal bar
    for y_bar in range(input_grid.shape[1]):
        if np.all(input_grid[:, y_bar] == Color.YELLOW):
            break

    top_mask = input_grid[:, :y_bar]
    bottom_mask = input_grid[:, y_bar+1:]

    # Rotate the bottom mask 90 degrees clockwise
    rotated_bottom_mask = np.rot90(bottom_mask, k=-1)

    # Ensure the rotated mask has the same shape as the top mask
    if rotated_bottom_mask.shape != top_mask.shape:
        pad_width = ((0, max(0, top_mask.shape[0] - rotated_bottom_mask.shape[0])),
                     (0, max(0, top_mask.shape[1] - rotated_bottom_mask.shape[1])))
        rotated_bottom_mask = np.pad(rotated_bottom_mask, pad_width, mode='constant', constant_values=Color.BLACK)
        rotated_bottom_mask = rotated_bottom_mask[:top_mask.shape[0], :top_mask.shape[1]]

    # Perform XOR operation
    output_grid = np.zeros_like(top_mask)
    output_grid[(top_mask == Color.RED) ^ (rotated_bottom_mask == Color.BLUE)] = Color.GREEN
    
    return output_grid

def generate_input() -> np.ndarray:
    # Create a pair of bitmasks with different sizes
    width1, height1 = np.random.randint(3, 8), np.random.randint(3, 8)
    width2, height2 = np.random.randint(3, 8), np.random.randint(3, 8)

    grid1 = np.zeros((width1, height1), dtype=int)
    grid2 = np.zeros((width2, height2), dtype=int)

    for x in range(width1):
        for y in range(height1):
            grid1[x, y] = np.random.choice([Color.RED, Color.BLACK])

    for x in range(width2):
        for y in range(height2):
            grid2[x, y] = np.random.choice([Color.BLUE, Color.BLACK])

    # Create a yellow horizontal bar
    bar = np.full((1, max(height1, height2)), Color.YELLOW)

    # Combine the grids and bar
    grid = np.vstack((grid1, bar, grid2))

    return grid