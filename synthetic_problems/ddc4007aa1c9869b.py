from common import *

import numpy as np
from typing import *

# concepts:
# reflection, color, bitmasks with separator, logical operations

# description:
# In the input, you will see two color bitmasks separated by a grey vertical bar.
# To make the output, reflect the left half vertically, and color the overlapping regions with teal color if they match in both bitmasks after reflection.

def main(input_grid):
    # Find the grey vertical bar. Vertical means constant X
    for x_bar in range(input_grid.shape[0]):
        if np.all(input_grid[x_bar, :] == Color.GREY):
            break

    left_mask = input_grid[:x_bar, :]
    right_mask = input_grid[x_bar+1:, :]
    
    # Reflect the left mask vertically
    reflected_left_mask = left_mask[:, ::-1]

    output_grid = np.zeros_like(left_mask)
    matching_mask = reflected_left_mask == right_mask

    # Color the matching regions with teal.
    output_grid[matching_mask] = Color.TEAL
    
    # Place the left and right halves with the bar back into output grid
    output_with_bar = np.concatenate((left_mask, np.full((1, left_mask.shape[1]), Color.GREY), right_mask), axis=0)
    
    # Overwrite the overlap area with the output grid reflecting the matching regions
    output_with_bar[:x_bar, :] = output_grid
    output_with_bar[x_bar+1:, :] = right_mask

    return output_with_bar

def generate_input():
    # create a pair of equally sized maroon bitmasks
    width, height = np.random.randint(2, 10), np.random.randint(5, 10)
    
    colors = [Color.BLUE, Color.RED, Color.GREEN, Color.YELLOW, Color.PINK, Color.ORANGE, Color.TEAL, Color.MAROON]

    left_mask = np.random.choice(colors + [Color.BLACK], (width, height))
    right_mask = np.random.choice(colors + [Color.BLACK], (width, height))
    
    # create a grey vertical bar
    bar = np.zeros((1, height), dtype=int)
    bar[0, :] = Color.GREY

    grid = np.concatenate((left_mask, bar, right_mask), axis=0)

    return grid