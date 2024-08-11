from common import *

import numpy as np
from typing import *

# concepts:
# bitmasks with separator, boolean logical operations, symmetry, color guide

# description:
# The input grid consists of two square patterns separated by a vertical yellow line.
# Each pattern is made up of red and black pixels.
# To create the output:
# 1. Perform an XOR operation between the left pattern and the vertical mirror of the right pattern.
# 2. Where the XOR result is true (different), color the output green.
# 3. Where the XOR result is false (same), color the output blue.
# The output should be a single square pattern of the same size as each input pattern.

def main(input_grid):
    height, width = input_grid.shape
    
    # Find the yellow vertical line
    for x_bar in range(width):
        if np.all(input_grid[:, x_bar] == Color.YELLOW):
            break
    
    # Extract left and right patterns
    left_pattern = input_grid[:, :x_bar]
    right_pattern = input_grid[:, x_bar+1:]
    
    # Mirror the right pattern
    mirrored_right = np.fliplr(right_pattern)
    
    # Initialize output grid
    output_grid = np.zeros_like(left_pattern)
    
    # Perform XOR operation and apply color mapping
    xor_result = (left_pattern != mirrored_right)
    output_grid[xor_result] = Color.GREEN
    output_grid[~xor_result] = Color.BLUE
    
    return output_grid

def generate_input():
    # Define the size of each pattern (square)
    size = np.random.randint(5, 9)
    
    # Initialize the input grid
    input_grid = np.full((size, size * 2 + 1), Color.BLACK)
    
    # Generate left pattern
    left_pattern = np.random.choice([Color.BLACK, Color.RED], size=(size, size))
    
    # Generate right pattern (ensuring it's different from left)
    right_pattern = np.random.choice([Color.BLACK, Color.RED], size=(size, size))
    while np.array_equal(left_pattern, right_pattern):
        right_pattern = np.random.choice([Color.BLACK, Color.RED], size=(size, size))
    
    # Place patterns in the input grid
    input_grid[:, :size] = left_pattern
    input_grid[:, size+1:] = right_pattern
    
    # Add yellow separator
    input_grid[:, size] = Color.YELLOW
    
    return input_grid