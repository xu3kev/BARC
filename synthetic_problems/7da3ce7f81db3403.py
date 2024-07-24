import numpy as np
from typing import *
from common import *

# concepts:
# bitmasks with separator, boolean logical operations

# description:
# In the input, you will see two blue bitmasks separated by a grey vertical bar.
# To make the output, flip colors on the right side bitmask according to the complement of the left bitmask:
#     if left is blue, right stays the same.
#     if left is black, flip the right blue pixel to red and the black to blue.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the grey vertical bar. Vertical means constant X
    for x_bar in range(input_grid.shape[0]):
        if np.all(input_grid[x_bar, :] == Color.GREY):
            break

    left_mask = input_grid[:x_bar, :]
    right_mask = input_grid[x_bar+1:, :]

    output_grid = np.zeros_like(right_mask)
    
    # Perform the flipping transformation
    output_grid[(left_mask == Color.BLACK) & (right_mask == Color.BLUE)] = Color.RED
    output_grid[(left_mask == Color.BLACK) & (right_mask == Color.BLACK)] = Color.BLUE
    output_grid[(left_mask == Color.BLUE) & (right_mask == Color.BLUE)] = Color.BLUE
    output_grid[(left_mask == Color.BLUE) & (right_mask == Color.BLACK)] = Color.BLACK
    
    return output_grid


def generate_input() -> np.ndarray:
    # create a pair of equally sized bitmasks
    width, height = np.random.randint(2, 10), np.random.randint(2, 10)

    grid1 = np.zeros((width, height), dtype=int)
    grid2 = np.zeros((width, height), dtype=int)

    for x in range(width):
        for y in range(height):
            grid1[x, y] = np.random.choice([Color.BLUE, Color.BLACK])
            grid2[x, y] = np.random.choice([Color.BLUE, Color.BLACK])
    
    # create a grey vertical bar
    bar = np.zeros((1, height), dtype=int)
    bar[0, :] = Color.GREY

    grid = np.concatenate((grid1, bar, grid2), axis=0)

    return grid