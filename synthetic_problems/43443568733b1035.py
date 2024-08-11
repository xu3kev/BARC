from common import *

import numpy as np
from typing import *

# concepts:
# patterns, colors as indicators, repeating patterns

# description:
# In the input grid, you will find a random arrangement of colors on a black background.
# Each color serves as an indicator for a unique pattern sprouting from that location.
# For each colored pixel in the input grid, copy a predefined small pattern onto the corresponding position in the output grid.
# Ensure that patterns can overlap but not overwrite each other, giving precedence to the first pattern placed.

def main(input_grid):
    # First, get the grid size
    n, m = input_grid.shape

    # Determine the background color (most common color)
    background_color = np.bincount(input_grid.flatten()).argmax()

    # Define small unique patterns for each color except black
    def create_pattern(color):
        pattern_size = 3
        pattern = np.full((pattern_size, pattern_size), background_color)
        pattern[1, 1] = color
        pattern[1, 2] = color
        pattern[2, 1] = color
        return pattern

    patterns = {color: create_pattern(color) for color in Color.NOT_BLACK}

    output_grid = np.full((n, m), background_color)

    for x in range(n):
        for y in range(m):
            if input_grid[x, y] != background_color:
                pattern = patterns[input_grid[x, y]]
                blit_sprite(output_grid, pattern, x - 1, y - 1, background=background_color)

    return output_grid

def generate_input():
    # Define grid size
    n, m = np.random.randint(5, 10, size=2)
    input_grid = np.full((n, m), Color.BLACK)

    # Randomly place colored pixels
    num_colors = np.random.randint(3, 6)
    colors = np.random.choice(list(Color.NOT_BLACK), num_colors, replace=False)
    
    for _ in range(np.random.randint(5, 15)):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        input_grid[x, y] = np.random.choice(colors)

    return input_grid