import numpy as np
from typing import *
from common import *

# concepts:
# bitmasks with separator, boolean logical operations, color guide, counting

# description:
# In the input you will see three colored bitmasks separated by two grey horizontal bars
# The top bitmask is always red, the middle is always green, and the bottom is always blue
# To make the output, apply the following rules:
# 1. If all three bitmasks have a pixel set (logical AND), color that pixel yellow
# 2. If exactly two bitmasks have a pixel set, color that pixel orange
# 3. If only one bitmask has a pixel set, color that pixel pink
# 4. If no bitmasks have a pixel set, leave that pixel black

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find the grey horizontal bars
    bar_indices = []
    for y in range(input_grid.shape[1]):
        if np.all(input_grid[:, y] == Color.GREY):
            bar_indices.append(y)
    
    assert len(bar_indices) == 2, "Expected two grey horizontal bars"

    # Extract the three bitmasks
    red_mask = input_grid[:, :bar_indices[0]]
    green_mask = input_grid[:, bar_indices[0]+1:bar_indices[1]]
    blue_mask = input_grid[:, bar_indices[1]+1:]

    # Create the output grid
    output_grid = np.zeros_like(red_mask)

    # Apply the rules
    all_set = (red_mask == Color.RED) & (green_mask == Color.GREEN) & (blue_mask == Color.BLUE)
    two_set = ((red_mask == Color.RED) & (green_mask == Color.GREEN) & (blue_mask != Color.BLUE)) | \
              ((red_mask == Color.RED) & (green_mask != Color.GREEN) & (blue_mask == Color.BLUE)) | \
              ((red_mask != Color.RED) & (green_mask == Color.GREEN) & (blue_mask == Color.BLUE))
    one_set = (red_mask == Color.RED) ^ (green_mask == Color.GREEN) ^ (blue_mask == Color.BLUE)

    output_grid[all_set] = Color.YELLOW
    output_grid[two_set] = Color.ORANGE
    output_grid[one_set] = Color.PINK

    return output_grid

def generate_input() -> np.ndarray:
    # Create three equally sized bitmasks
    width, height = np.random.randint(3, 8), np.random.randint(3, 8)

    red_mask = np.random.choice([Color.RED, Color.BLACK], size=(width, height))
    green_mask = np.random.choice([Color.GREEN, Color.BLACK], size=(width, height))
    blue_mask = np.random.choice([Color.BLUE, Color.BLACK], size=(width, height))

    # Create grey horizontal bars
    bar = np.full((width, 1), Color.GREY)

    # Combine the masks and bars
    grid = np.hstack((red_mask, bar, green_mask, bar, blue_mask))

    return grid