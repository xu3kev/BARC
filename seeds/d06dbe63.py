from common import *

import numpy as np
from typing import *

# concepts:
# staircase pattern

# description:
# In the input you will see a single teal pixel.
# To make the output, draw a staircase from the teal pixel to the upper right and lower left with a step size of 2.

def main(input_grid):
    # Find the location of the teal pixel
    teal_x, teal_y = np.argwhere(input_grid == Color.TEAL)[0]

    # staircase is gray
    staircase_color = Color.GRAY

    # we are going to draw on top of the input
    output_grid = input_grid.copy()
    width, height = input_grid.shape

    # Draw stairs from the teal pixel
    STAIR_LEN = 2
    # First draw stair to the upper right
    x, y = teal_x, teal_y
    while 0 <= x < width and 0 <= y < height:
        # go up
        draw_line(output_grid, x, y, length=STAIR_LEN, color=staircase_color, direction=(0, -1))
        y -= STAIR_LEN
        # go right
        draw_line(output_grid, x, y, length=STAIR_LEN, color=staircase_color, direction=(1, 0))
        x += STAIR_LEN
    
    # Then draw stair to the lower left
    x, y = teal_x, teal_y
    while 0 <= x < width and 0 <= y < height:
        # go down
        draw_line(output_grid, x, y, length=STAIR_LEN, color=staircase_color, direction=(0, 1))
        y += STAIR_LEN
        # go left
        draw_line(output_grid, x, y, length=STAIR_LEN, color=staircase_color, direction=(-1, 0))
        x -= STAIR_LEN
    
    # make sure that the teal pixel stays there
    output_grid[teal_x, teal_y] = Color.TEAL

    return output_grid

def generate_input():
    # Generate grid
    width, height = np.random.randint(15, 25), np.random.randint(15, 25)
    grid = np.zeros((width, height), dtype=int)

    # Randomly place one teal pixel on the grid
    # Ensure the pixel is not on the border
    x, y = np.random.randint(width // 3, width * 2 // 3), np.random.randint(height // 3, height * 2 // 3)
    grid[x, y] = Color.TEAL

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
