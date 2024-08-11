from common import *

import numpy as np
from typing import *

# concepts:
# bitmasks with separator, boolean logical operations, color, alignment by color

# description:
# In the input, you will see two 8x8 blue and green patterns side-by-side separated by a vertical yellow line in the middle of the grid.
# To make the output, you have to overlap the two patterns. If a cell is blue in either the left or right patterns (but not both), then the corresponding cell in the output is colored red.
# If a cell is green in either the left or right patterns (but not both), then the corresponding cell in the output is colored orange.
# If the overlapping cells are both blue or both green, then the corresponding cell in the output is colored black.

def main(input_grid):

    width, height = input_grid.shape
   
    # Find the yellow vertical line/bar
    for x_bar in range(width):
        if np.all(input_grid[x_bar, :] == Color.YELLOW):
            break
    
    # Extract left and right patterns
    left_pattern = input_grid[:x_bar, :]
    right_pattern = input_grid[x_bar+1:, :] 

    output_grid = np.zeros_like(left_pattern)

    # Applying the logical operations as per the description
    red_pattern = (left_pattern == Color.BLUE) ^ (right_pattern == Color.BLUE)
    orange_pattern = (left_pattern == Color.GREEN) ^ (right_pattern == Color.GREEN)
    blue_pattern = (left_pattern == Color.BLUE) & (right_pattern == Color.BLUE)
    green_pattern = (left_pattern == Color.GREEN) & (right_pattern == Color.GREEN)

    output_grid[red_pattern] = Color.RED
    output_grid[orange_pattern] = Color.ORANGE
    output_grid[blue_pattern] = Color.BLACK
    output_grid[green_pattern] = Color.BLACK

    return output_grid


def generate_input():
    
    # Define the grid size
    width = 17  # 8 left + 1 yellow line + 8 right
    height = 8

    # Initialize an empty grid
    input_grid = np.full((width, height), Color.BLACK)

    # Randomly assign blue or green to the left and right patterns
    for x in range(width):
        for y in range(height):
            if x < 8 or x > 8:
                input_grid[x, y] = np.random.choice([Color.BLUE, Color.GREEN, Color.BLACK])

    # Set the yellow vertical line
    input_grid[8, :] = Color.YELLOW

    return input_grid