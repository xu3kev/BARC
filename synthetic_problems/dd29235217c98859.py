import numpy as np
from typing import *
from common import *

# concepts:
# bitmasks with separator, boolean logical operations, symmetries

# description:
# In the input, you will see three bitmasks separated by grey horizontal bars:
# 1. A red bitmask at the top
# 2. A blue bitmask in the middle
# 3. A yellow bitmask at the bottom
# To make the output:
# 1. Apply XOR operation between the red and blue bitmasks
# 2. Apply OR operation between the result and the yellow bitmask
# 3. Color the resulting 1s in teal
# 4. Finally, apply vertical symmetry to the entire output

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the grey horizontal bars
    bar_indices = []
    for y in range(input_grid.shape[1]):
        if np.all(input_grid[:, y] == Color.GREY):
            bar_indices.append(y)

    assert len(bar_indices) == 2, "Expected two separator bars"

    # Extract the three bitmasks
    red_mask = input_grid[:, :bar_indices[0]]
    blue_mask = input_grid[:, bar_indices[0]+1:bar_indices[1]]
    yellow_mask = input_grid[:, bar_indices[1]+1:]

    # Perform boolean operations
    xor_result = np.logical_xor(red_mask == Color.RED, blue_mask == Color.BLUE)
    final_result = np.logical_or(xor_result, yellow_mask == Color.YELLOW)

    # Create output grid and color the resulting 1s in teal
    output_grid = np.full_like(red_mask, Color.BLACK)
    output_grid[final_result] = Color.TEAL

    # Apply vertical symmetry
    output_grid = np.concatenate((output_grid, np.fliplr(output_grid)), axis=1)

    return output_grid

def generate_input() -> np.ndarray:
    width, height = np.random.randint(3, 8), np.random.randint(3, 8)

    def create_bitmask(color):
        mask = np.full((width, height), Color.BLACK)
        mask[np.random.random((width, height)) < 0.5] = color
        return mask

    red_mask = create_bitmask(Color.RED)
    blue_mask = create_bitmask(Color.BLUE)
    yellow_mask = create_bitmask(Color.YELLOW)

    # Create grey horizontal bars
    bar = np.full((width, 1), Color.GREY)

    # Combine all elements
    grid = np.concatenate((red_mask, bar, blue_mask, bar, yellow_mask), axis=1)

    return grid