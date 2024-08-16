from common import *

import numpy as np
from typing import *

# concepts:
# patterns, objects, spiral formation

# description:
# In the input grid, you will see a single colored pixel (non-black) scattered anywhere in the grid.
# To make the output, generate a spiral path starting from that pixel and continue until 
# the entire grid is filled with pixels of the same color as the starting pixel.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Find the starting colored pixel
    colored_x, colored_y = np.argwhere(input_grid != Color.BLACK)[0]
    color = input_grid[colored_x, colored_y]
    
    # Define spiral directions: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    x, y = colored_x, colored_y
    steps_left = 1
    dir_idx = 0
    steps_taken = 0
    
    while steps_left < max(output_grid.shape) * 2:
        for _ in range(steps_left):
            if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1] and output_grid[x, y] == Color.BLACK:
                output_grid[x, y] = color

            x += directions[dir_idx][0]
            y += directions[dir_idx][1]
            steps_taken += 1

            if steps_taken >= output_grid.size:
                return output_grid
        
        dir_idx = (dir_idx + 1) % 4
        if dir_idx % 2 == 0:
            steps_left += 1
    
    return output_grid

def generate_input():
    n = np.random.randint(6, 15)
    m = np.random.randint(6, 15)
    grid = np.zeros((n, m), dtype=int)

    color = np.random.choice(list(Color.NOT_BLACK))

    colored_x = np.random.randint(0, n)
    colored_y = np.random.randint(0, m)
    grid[colored_x, colored_y] = color

    return grid