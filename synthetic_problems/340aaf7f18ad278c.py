from common import *

import numpy as np
from typing import *

# concepts:
# patterns, repetition, color change

# description:
# In the input you will see distinct 3x3 objects of varying colors. 
# For the first row, replicate the 3x3 object as a pattern, filling the entire row's width.
# For each subsequent row, repeat the process, but shift the pattern by one column to the right, wrapping around the edge of the grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    n, m = input_grid.shape

    # Size of the repeating pattern
    pattern_size = 3

    # Prepare the output grid
    output_grid = np.full((n, m), Color.BLACK)

    # Define a function to replicate a pattern across a row
    def replicate_pattern(grid, pattern, y_offset):
        num_repeats = m // pattern_size + 1  # Ensure the pattern wraps around
        pattern_row = np.tile(pattern, (1, num_repeats))[:, :m]

        # Adjust the offset for each row to create the wrapping effect
        pattern_row = np.roll(pattern_row, y_offset * pattern_size, axis=1)

        # Populate the output grid with the pattern, row by row
        for i in range(pattern_size):
            output_grid[y_offset * pattern_size + i] = pattern_row[i]

    # Extract each 3x3 object and apply the pattern
    for y in range(n // pattern_size):
        for x in range(m // pattern_size):
            pattern = input_grid[y * pattern_size:(y + 1) * pattern_size, x * pattern_size:(x + 1) * pattern_size]
            replicate_pattern(output_grid, pattern, y)

    return output_grid

def generate_input() -> np.ndarray:
    n, m = 21, 21  # Size of the grid, should be a multiple of 3
    grid = np.full((n, m), Color.BLACK)

    # Define a 3x3 sprite generator
    def random_3x3_sprite():
        sprite_color = np.random.choice(Color.NOT_BLACK)
        sprite = np.random.choice([Color.BLACK, sprite_color], (3, 3), p=[0.5, 0.5])
        return sprite

    # Populate the grid with distinct 3x3 objects
    for y in range(n // 3):
        for x in range(m // 3):
            sprite = random_3x3_sprite()
            blit_sprite(grid, sprite, y * 3, x * 3, background=Color.BLACK)

    return grid