from common import *

import numpy as np
from typing import *

# concepts:
# lines, colors as indicators

# description:
# In the input, you will see a red pixel and a teal pixel.
# To make the output, draw a horizontal yellow line from the red pixel to the column of the teal pixel, then draw a vertical yellow line from there to the teal pixel.
# However, if the red and teal pixels share the same row or column, draw a blue line instead.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # find the red and teal pixels
    red_x, red_y = np.where(input_grid == Color.RED)
    teal_x, teal_y = np.where(input_grid == Color.TEAL)

    # check if the red and teal pixels are in the same row or column
    if red_x[0] == teal_x[0] or red_y[0] == teal_y[0]:
        # draw a blue line directly from the red pixel to the teal pixel
        if red_x[0] == teal_x[0]:
            # Same row, draw a horizontal blue line
            direction = (1 if red_y[0] < teal_y[0] else -1, 0)
            draw_line(output_grid, red_x[0], red_y[0] + direction[0], length=abs(teal_y[0] - red_y[0]) - 1, color=Color.BLUE, direction=direction)
        else:
            # Same column, draw a vertical blue line
            direction = (0, 1 if red_x[0] < teal_x[0] else -1)
            draw_line(output_grid, red_x[0] + direction[1], red_y[0], length=abs(teal_x[0] - red_x[0]) - 1, color=Color.BLUE, direction=direction)
    else:
        # draw the horizontal yellow line from the red pixel to the column of the teal pixel
        direction = (1, 0) if red_y[0] < teal_y[0] else (-1, 0)
        draw_line(output_grid, red_x[0], red_y[0] + direction[1], length=abs(teal_y[0] - red_y[0]), color=Color.YELLOW, direction=direction)
        
        # draw the vertical yellow line from the end of the horizontal yellow line to the teal pixel
        direction = (0, 1) if red_x[0] < teal_x[0] else (0, -1)
        draw_line(output_grid, teal_x[0], red_y[0], length=abs(teal_x[0] - red_x[0]), color=Color.YELLOW, direction=direction)
    
    return output_grid

def generate_input():
    # make a black grid as the background
    n = np.random.randint(6, 15)
    m = np.random.randint(6, 15)
    grid = np.zeros((n, m), dtype=int)

    # select a random position for the red pixel
    red_x = np.random.randint(0, n)
    red_y = np.random.randint(0, m)
    grid[red_x, red_y] = Color.RED

    # select a random position for the teal pixel
    teal_x = np.random.randint(0, n)
    teal_y = np.random.randint(0, m)
    grid[teal_x, teal_y] = Color.TEAL

    # ensure that the red and teal pixels are not at the same position
    if (red_x == teal_x and red_y == teal_y):
        return generate_input()
    
    return grid