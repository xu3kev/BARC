from common import *

import numpy as np
from typing import *

# concepts:
# lines, patterns, scaling, connectivity

# description:
# In the input, you see several blue pixels placed on a black background.
# For each blue pixel, draw a green square of size 3x3 around it.
# Then, connect all blue pixels with green lines in a zigzag manner, avoiding overlapping with the squares.
# If any square overlaps, adjust the lines to avoid the overlap and continue the zigzag pattern.  

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # get the coordinates of the blue pixels
    blue_coords = np.argwhere(input_grid == Color.BLUE)
    
    # define the square size
    square_size = 3

    # draw green squares around blue pixels
    for x, y in blue_coords:
        for i in range(-(square_size // 2), (square_size // 2) + 1):
            for j in range(-(square_size // 2), (square_size // 2) + 1):
                if 0 <= x + i < input_grid.shape[0] and 0 <= y + j < input_grid.shape[1]:
                    output_grid[x + i, y + j] = Color.GREEN

    # connect blue pixels with green lines in zigzag manner avoiding overlapping with squares
    if len(blue_coords) > 1:
        for i in range(len(blue_coords) - 1):
            start_x, start_y = blue_coords[i]
            end_x, end_y = blue_coords[i+1]

            # draw horizontal line
            direction = (0, 1) if start_y < end_y else (0, -1)
            draw_line(output_grid, start_x, start_y + direction[1], length=abs(end_y - start_y), color=Color.GREEN, direction=direction)

            # draw vertical line
            direction = (1, 0) if start_x < end_x else (-1, 0)
            draw_line(output_grid, start_x + direction[0] * abs(end_x - start_x), end_y, length=abs(end_x - start_x), color=Color.GREEN, direction=direction)
    
    return output_grid


def generate_input():
    # create a black grid as the background
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # randomly place a few blue pixels on the grid
    num_blue_pixels = np.random.randint(2, 6)
    for _ in range(num_blue_pixels):
        x, y = np.random.randint(n), np.random.randint(m)
        grid[x, y] = Color.BLUE
        
    return grid