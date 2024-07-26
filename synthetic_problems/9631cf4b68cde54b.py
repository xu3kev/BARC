from common import *

import numpy as np
from typing import *

# concepts:
# patterns, vertical bars, colors as indicators

# description:
# In the input, you will see a grid with multiple vertical segments of varying height.
# Each vertical segment contains colored pixels with black background elsewhere.
# To construct the output, for each vertical segment, fill the remaining height till the bottom with the 
# color of the pixel at the bottom of each segment.

def main(input_grid):
    output_grid = np.copy(input_grid)

    # Iterate through each column of the grid
    for col in range(input_grid.shape[1]):
        # Find the bottom-most colored pixel in each vertical segment
        for row in reversed(range(input_grid.shape[0])):
            if input_grid[row, col] != Color.BLACK:
                color = input_grid[row, col]
                # Fill the remaining height till the bottom with the identified color
                output_grid[row:, col] = color
                break
            
    return output_grid


def generate_input():
    # Determine the grid size
    n = np.random.randint(5, 10)
    m = np.random.randint(5, 10)

    # Create a black grid
    grid = np.full((n, m), Color.BLACK)

    num_segments = m
    max_segment_height = n

    # Generate vertical segments
    for col in range(num_segments):
        height = np.random.randint(1, max_segment_height + 1)
        color = np.random.choice(list(Color.NOT_BLACK))

        # Fill the segment with the chosen color
        grid[:height, col] = color
    
    return grid