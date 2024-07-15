from common import *

import numpy as np
from typing import *

# concepts:
# boolean logical operations, bitmasks with separator, sliding objects

# description:
# In the input you will see two maroon bitmasks separated by a blue vertical bar
# First, produce a new bitmask by taking the logical AND of the maroon pixels from both bitmasks
# Then, move this resulting bitmask one pixel down in the output grid

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the blue vertical bar. Vertical means constant X
    for x_bar in range(input_grid.shape[0]):
        if np.all(input_grid[x_bar, :] == Color.BLUE):
            break

    left_mask = input_grid[:x_bar, :]
    right_mask = input_grid[x_bar+1:, :]

    # Create the AND bitmask
    and_mask = (left_mask == Color.MAROON) & (right_mask == Color.MAROON)
    merged_mask = np.zeros_like(left_mask)
    merged_mask[and_mask] = Color.MAROON

    # Slide down by one pixel
    output_grid = translate(merged_mask, 0, 1, background=Color.BLACK)

    return output_grid

def generate_input() -> np.ndarray:
    # create a pair of equally sized maroon bitmasks
    width, height = np.random.randint(2, 10), np.random.randint(2, 10)

    grid1 = np.zeros((width, height), dtype=int)
    grid2 = np.zeros((width, height), dtype=int)

    for x in range(width):
        for y in range(height):
            grid1[x, y] = np.random.choice([Color.MAROON, Color.GREY, Color.BLACK])
            grid2[x, y] = np.random.choice([Color.MAROON, Color.GREY, Color.BLACK])
    
    # create a blue vertical bar
    bar = np.zeros((1, height), dtype=int)
    bar[0, :] = Color.BLUE

    grid = np.concatenate((grid1, bar, grid2), axis=0)

    return grid