import numpy as np
from typing import *
from common import *

# concepts:
# bitmasks with separator, boolean logical operations, Coloring diagonal pixels, sprites

# description:
# In the input, you will see two maroon bitmasks separated by a blue vertical bar.
# To make the output, find the logical XOR of the two bitmasks and color the pixels of the result teal.
# Then color all the diagonal pixels around the teal pixels (result of the XOR) that are still black as pink.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the blue vertical bar. Vertical means constant X
    for x_bar in range(input_grid.shape[0]):
        if np.all(input_grid[x_bar, :] == Color.BLUE):
            break

    left_mask = input_grid[:x_bar, :]
    right_mask = input_grid[x_bar+1:, :]

    # Perform XOR operation on the two masks
    xor_result = (left_mask != Color.MAROON) ^ (right_mask != Color.MAROON)

    # Initialize the output grid with black
    output_grid = np.zeros_like(left_mask)

    # Color the XOR result pixels teal
    output_grid[xor_result] = Color.TEAL

    # Create diagonal directions
    diagonal_deltas = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    # Color diagonal pixels around the teal pixels pink if they are black
    for x in range(output_grid.shape[0]):
        for y in range(output_grid.shape[1]):
            if output_grid[x, y] == Color.TEAL:
                for dx, dy in diagonal_deltas:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < output_grid.shape[0] and 0 <= ny < output_grid.shape[1]:
                        if output_grid[nx, ny] == Color.BLACK:
                            output_grid[nx, ny] = Color.PINK
    
    return output_grid


def generate_input() -> np.ndarray:
    # create a pair of maroon bitmasks
    width, height = np.random.randint(2, 10), np.random.randint(2, 10)

    grid1 = np.zeros((width, height), dtype=int)
    grid2 = np.zeros((width, height), dtype=int)

    for x in range(width):
        for y in range(height):
            grid1[x, y] = np.random.choice([Color.MAROON, Color.BLACK])
            grid2[x, y] = np.random.choice([Color.MAROON, Color.BLACK])
    
    # create a blue vertical bar
    bar = np.zeros((1, height), dtype=int)
    bar[0, :] = Color.BLUE

    grid = np.concatenate((grid1, bar, grid2), axis=0)

    return grid