import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, bitmasks with separator, color mapping

# description:
# The input consists of two bitmasks separated by an orange vertical bar.
# The left bitmask uses red for 1 and black for 0.
# The right bitmask uses blue for 1 and black for 0.
# To create the output:
# 1. Perform a logical XOR operation between the two bitmasks.
# 2. In the result, color the '1' pixels green where the left mask was 1 (red),
#    and yellow where the right mask was 1 (blue).
# 3. The '0' pixels in the result remain black.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the orange vertical bar
    for x_bar in range(input_grid.shape[1]):
        if np.all(input_grid[:, x_bar] == Color.ORANGE):
            break

    left_mask = input_grid[:, :x_bar]
    right_mask = input_grid[:, x_bar+1:]

    # Create boolean masks
    left_bool = (left_mask == Color.RED)
    right_bool = (right_mask == Color.BLUE)

    # Perform XOR operation
    xor_result = np.logical_xor(left_bool, right_bool)

    # Create output grid
    output_grid = np.zeros_like(xor_result, dtype=int)
    output_grid[xor_result & left_bool] = Color.GREEN
    output_grid[xor_result & right_bool] = Color.YELLOW

    return output_grid

def generate_input() -> np.ndarray:
    height = np.random.randint(3, 8)
    width = np.random.randint(3, 8)

    left_mask = np.random.choice([Color.RED, Color.BLACK], size=(height, width))
    right_mask = np.random.choice([Color.BLUE, Color.BLACK], size=(height, width))

    # Create orange separator
    separator = np.full((height, 1), Color.ORANGE)

    # Combine masks and separator
    input_grid = np.hstack((left_mask, separator, right_mask))

    return input_grid