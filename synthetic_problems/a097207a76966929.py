from common import *

import numpy as np
from typing import *

# concepts:
# gravitational collapse, objects

# description:
# In the input grid, colored single pixels and blocks of pixels are scattered. 
# To make the output, simulate a gravitational collapse by letting all colored pixels fall downwards until they rest on the bottom of the grid or on top of other pixels.

def main(input_grid):
    """
    This function takes an input grid of colored pixels scattered around and lets them fall under the effect of gravity.
    """
    output_grid = input_grid.copy()
    n, m = output_grid.shape

    for col in range(m):
        stack_height = n - 1  # Start stacking from the bottom row
        for row in reversed(range(n)):
            if output_grid[row, col] != Color.BLACK:
                # Move the colored pixel downward to the 'stack_height' row
                output_grid[stack_height, col] = output_grid[row, col]
                if stack_height != row:  # if it's not already in the correct position
                    output_grid[row, col] = Color.BLACK
                stack_height -= 1

    return output_grid

def generate_input():
    """
    Generates a random input grid with scattered colored pixels and blocks.
    """
    n = np.random.randint(10, 15)
    m = np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)
    
    num_objects = np.random.randint(5, 10)
    for _ in range(num_objects):
        # Randomly choose a size for the object (single pixel or small block)
        block_height = np.random.randint(1, 3)
        block_width = np.random.randint(1, 3)

        # Create a block with a random color
        color = np.random.choice(list(Color.NOT_BLACK))
        block = np.full((block_height, block_width), color)

        # Find a random location to place the block
        x, y = np.random.randint(0, n-block_height+1), np.random.randint(0, m-block_width+1)

        # Place the block on the grid
        blit(grid, block, x, y)

    return grid