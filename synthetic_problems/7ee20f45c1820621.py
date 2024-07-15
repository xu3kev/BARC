import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, bitmasks with separator, counting, color

# description:
# In the input you will see two bitmasks separated by a yellow horizontal bar.
# The left bitmask uses red pixels, and the right bitmask uses blue pixels.
# To make the output:
# 1. Perform a logical XOR operation between the two bitmasks
# 2. Count the number of 'on' pixels in the resulting XOR mask
# 3. Color the output grid based on this count:
#    - If the count is odd, fill the entire output with green
#    - If the count is even, fill the entire output with orange

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the yellow horizontal bar
    for y_bar in range(input_grid.shape[1]):
        if np.all(input_grid[:, y_bar] == Color.YELLOW):
            break

    top_mask = input_grid[:, :y_bar]
    bottom_mask = input_grid[:, y_bar+1:]

    # Perform XOR operation
    xor_result = np.logical_xor(top_mask == Color.RED, bottom_mask == Color.BLUE)

    # Count 'on' pixels
    on_pixel_count = np.sum(xor_result)

    # Create output grid
    output_grid = np.zeros_like(top_mask)
    if on_pixel_count % 2 == 1:  # odd
        output_grid[:, :] = Color.GREEN
    else:  # even
        output_grid[:, :] = Color.ORANGE
    
    return output_grid


def generate_input() -> np.ndarray:
    # create a pair of equally sized bitmasks
    width, height = np.random.randint(3, 8), np.random.randint(3, 8)

    grid1 = np.zeros((width, height), dtype=int)
    grid2 = np.zeros((width, height), dtype=int)

    for x in range(width):
        for y in range(height):
            grid1[x, y] = np.random.choice([Color.RED, Color.BLACK])
            grid2[x, y] = np.random.choice([Color.BLUE, Color.BLACK])
    
    # create a yellow horizontal bar
    bar = np.zeros((width, 1), dtype=int)
    bar[:, 0] = Color.YELLOW

    grid = np.concatenate((grid1, bar, grid2), axis=1)

    return grid