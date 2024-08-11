import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, bitmasks with separator, pixel manipulation, growing

# description:
# In the input you will see two bitmasks separated by a grey horizontal bar
# The left bitmask uses red pixels, the right bitmask uses blue pixels
# To make the output:
# 1. Perform a logical XOR operation between the two bitmasks
# 2. For each resulting 'true' pixel, grow it by 1 pixel in all 8 directions (if possible)
# 3. Color the resulting pixels yellow

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the grey horizontal bar
    for y_bar in range(input_grid.shape[1]):
        if np.all(input_grid[:, y_bar] == Color.GREY):
            break

    top_mask = input_grid[:, :y_bar]
    bottom_mask = input_grid[:, y_bar+1:]

    # Perform XOR operation
    xor_result = np.logical_xor(top_mask == Color.RED, bottom_mask == Color.BLUE)

    # Create output grid
    output_grid = np.full_like(top_mask, Color.BLACK)

    # Grow and color the XOR result
    height, width = xor_result.shape
    for x in range(height):
        for y in range(width):
            if xor_result[x, y]:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width:
                            output_grid[nx, ny] = Color.YELLOW

    return output_grid

def generate_input() -> np.ndarray:
    # create a pair of equally sized bitmasks
    width, height = np.random.randint(5, 15), np.random.randint(5, 15)

    grid1 = np.zeros((height, width), dtype=int)
    grid2 = np.zeros((height, width), dtype=int)

    for x in range(height):
        for y in range(width):
            grid1[x, y] = np.random.choice([Color.RED, Color.BLACK])
            grid2[x, y] = np.random.choice([Color.BLUE, Color.BLACK])
    
    # create a grey horizontal bar
    bar = np.zeros((height, 1), dtype=int)
    bar[:, 0] = Color.GREY

    grid = np.concatenate((grid1, bar, grid2), axis=1)

    return grid