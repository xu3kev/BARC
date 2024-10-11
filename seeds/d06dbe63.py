from common import *

import numpy as np
from typing import *

# concepts:
# draw line, stair pattern

# description:
# In the input you will see a grid with a teal pixel.
# To make the output, draw a stair line from the teal pixel to the upper right and lower left.

def main(input_grid):
    # Find the teal pixel
    x, y = np.where(input_grid == Color.TEAL)

    # Line color is gray
    line_color = Color.GRAY

    # Generate the output grid
    output_grid = input_grid.copy()
    n, m = input_grid.shape
    

    # Draw stair line from the teal pixel
    STAIR_LEN = 2
    # First draw stair line to the upper right
    cur_x, cur_y = x[0], y[0]
    if_vertical = True
    cur_stair_len = 0
    while True:
        # If the stair line is vertical, move up, otherwise move right
        if if_vertical:
            cur_y -= 1
        else:
            cur_x += 1

        # If the current position is out of the grid, stop drawing
        if cur_x < 0 or cur_x >= n or cur_y < 0 or cur_y >= m:
            break
        output_grid[cur_x][cur_y] = line_color

        # Periodically change the direction of the stair line
        cur_stair_len += 1
        if cur_stair_len == STAIR_LEN:
            if_vertical = not if_vertical
            cur_stair_len = 0

    # Then draw stair line to the lower left
    cur_x, cur_y = x[0], y[0]
    if_vertical = True
    cur_stair_len = 0
    while True:
        # If the stair line is vertical, move down, otherwise move left
        if if_vertical:
            cur_y += 1
        else:
            cur_x -= 1

        # If the current position is out of the grid, stop drawing
        if cur_x < 0 or cur_x >= n or cur_y < 0 or cur_y >= m:
            break

        output_grid[cur_x][cur_y] = line_color

        # Periodically change the direction of the stair line
        cur_stair_len += 1
        if cur_stair_len == STAIR_LEN:
            if_vertical = not if_vertical
            cur_stair_len = 0

    return output_grid


        

def generate_input():
    # Generate grid of size n x m
    n, m = np.random.randint(15, 25), np.random.randint(15, 25)
    grid = np.zeros((n, m), dtype=int)

    # Randomly place one teal pixel on the grid
    # Ensure the pixel is not on the border
    x, y = np.random.randint(n // 3, n * 2 // 3), np.random.randint(n // 3, n * 2 // 3)
    grid[x][y] = Color.TEAL

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
