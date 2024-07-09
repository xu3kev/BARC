import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, bitmasks with separator, color mapping

# description:
# In the input, you will see three bitmasks separated by two blue vertical bars. 
# The left bitmask is red, the middle one is green, and the right one is yellow.
# To make the output:
# 1. Perform a bitwise XOR operation between the left and middle bitmasks
# 2. Perform a bitwise AND operation between the result of step 1 and the right bitmask
# 3. In the final output, color the resulting '1' pixels orange, and '0' pixels teal

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the two blue vertical bars
    bar_positions = []
    for x in range(input_grid.shape[0]):
        if np.all(input_grid[x, :] == Color.BLUE):
            bar_positions.append(x)

    left_mask = input_grid[:bar_positions[0], :]
    middle_mask = input_grid[bar_positions[0]+1:bar_positions[1], :]
    right_mask = input_grid[bar_positions[1]+1:, :]

    # Convert color masks to boolean masks
    left_bool = (left_mask == Color.RED)
    middle_bool = (middle_mask == Color.GREEN)
    right_bool = (right_mask == Color.YELLOW)

    # Perform logical operations
    xor_result = np.logical_xor(left_bool, middle_bool)
    final_result = np.logical_and(xor_result, right_bool)

    # Create output grid
    output_grid = np.full_like(left_mask, Color.TEAL)
    output_grid[final_result] = Color.ORANGE
    
    return output_grid


def generate_input() -> np.ndarray:
    # Create three equally sized bitmasks
    width, height = np.random.randint(3, 8), np.random.randint(3, 8)

    grid1 = np.random.choice([Color.RED, Color.BLACK], size=(width, height))
    grid2 = np.random.choice([Color.GREEN, Color.BLACK], size=(width, height))
    grid3 = np.random.choice([Color.YELLOW, Color.BLACK], size=(width, height))
    
    # Create blue vertical bars
    bar = np.full((1, height), Color.BLUE)

    # Combine grids and bars
    grid = np.concatenate((grid1, bar, grid2, bar, grid3), axis=0)

    return grid