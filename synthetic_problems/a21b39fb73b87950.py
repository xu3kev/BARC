import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, bitmasks with separator, color mapping

# description:
# In the input, you will see three bitmasks separated by two vertical bars of different colors.
# The left bitmask uses yellow, the middle one uses green, and the right one uses pink.
# The separators are blue and orange vertical bars.
# To make the output:
# 1. Apply XOR operation between the left and middle bitmasks
# 2. Apply AND operation between the result and the right bitmask
# 3. In the final output, represent 'true' values with teal and 'false' values with gray

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the blue and orange vertical bars
    x_bar1, x_bar2 = None, None
    for x in range(input_grid.shape[0]):
        if np.all(input_grid[x, :] == Color.BLUE):
            x_bar1 = x
        elif np.all(input_grid[x, :] == Color.ORANGE):
            x_bar2 = x
            break

    left_mask = input_grid[:x_bar1, :]
    middle_mask = input_grid[x_bar1+1:x_bar2, :]
    right_mask = input_grid[x_bar2+1:, :]

    # XOR operation between left and middle masks
    xor_result = np.logical_xor(left_mask == Color.YELLOW, middle_mask == Color.GREEN)

    # AND operation with right mask
    final_result = np.logical_and(xor_result, right_mask == Color.PINK)

    # Create output grid
    output_grid = np.full_like(left_mask, Color.GRAY)
    output_grid[final_result] = Color.TEAL
    
    return output_grid


def generate_input() -> np.ndarray:
    # Create three equally sized bitmasks
    width, height = np.random.randint(3, 8), np.random.randint(3, 8)

    grid1 = np.random.choice([Color.YELLOW, Color.BLACK], size=(width, height))
    grid2 = np.random.choice([Color.GREEN, Color.BLACK], size=(width, height))
    grid3 = np.random.choice([Color.PINK, Color.BLACK], size=(width, height))
    
    # Create blue and orange vertical bars
    bar1 = np.full((1, height), Color.BLUE)
    bar2 = np.full((1, height), Color.ORANGE)

    # Combine all parts
    grid = np.concatenate((grid1, bar1, grid2, bar2, grid3), axis=0)

    return grid