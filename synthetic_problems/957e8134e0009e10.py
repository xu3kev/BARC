from common import *

import numpy as np
from typing import *
import random

# concepts:
# color guide, repetition, size

# description:
# In the input, you will see a grid divided into exactly two rows, each containing several non-overlapping square blocks of different colors. 
# The blocks in each row are separated by at least one black pixel. The output should be a grid where each block has been scaled up to twice its size
# while retaining its color and placed in the corresponding position relative to its original.

def main(input_grid):
    output_grid = np.zeros((input_grid.shape[0] * 2, input_grid.shape[1]), dtype=int)

    for y in range(0, input_grid.shape[1]):
        for x in range(0, input_grid.shape[0]):
            if input_grid[x, y] != Color.BLACK:
                color = input_grid[x, y]
                start_x = x * 2
                start_y = y
                output_grid[start_x:start_x + 2, start_y] = color
                output_grid[start_x, start_y + 1] = color
                output_grid[start_x + 1, start_y + 1] = color

    return output_grid

def generate_input():
    # generate parameters
    n = random.randint(10, 20)  # size of grid
    
    grid = np.zeros((n, n), dtype=int)

    colors = random.sample(list(Color.NOT_BLACK), random.randint(2, 5))
    block_size = random.randint(1, 3)
    
    def place_row(grid, y_start):
        x_start = random.randint(0, n - 2 * block_size - 1)
        for color in colors:
            for i in range(block_size):
                for j in range(block_size):
                    if x_start + i < n and y_start + j < n:
                        grid[x_start + i, y_start + j] = color
            x_start += block_size + random.randint(1, 2)
            if x_start + block_size >= n:
                break
    
    place_row(grid, 0)
    place_row(grid, block_size + random.randint(1, 2))
    
    return grid