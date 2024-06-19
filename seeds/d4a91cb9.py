from common import *

import numpy as np
from typing import *

# concepts:
# lines, color

# description:
# In the input you will see a red pixel and a teal pixel.
# To make the output, draw a horizontal yellow line from the red pixel to the column of the teal pixel, then draw a vertical yellow line from there to the teal pixel.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # find the red and teal pixels
    red_x, red_y = np.where(input_grid == Color.RED)
    teal_x, teal_y = np.where(input_grid == Color.TEAL)

    # draw the horizontal yellow line from the red pixel to the column the teal pixel is
    # figure out the direction of the line
    if red_x[0] < teal_x[0]:
        direction = (1, 0)
    else:
        direction = (-1, 0)
    # draw the line but don't draw over the red pixel
    draw_line(output_grid, red_x[0]+direction[0], red_y[0], length=np.abs(teal_x[0] - red_x[0]), color=Color.YELLOW, direction=direction)

    # draw the vertical yellow line from the end of the horizontal yellow line to the teal pixel
    # figure out the direction of the line
    if red_y[0] < teal_y[0]:
        direction = (0, 1)
    else:
        direction = (0, -1)
    # draw the line
    draw_line(output_grid, teal_x[0], red_y[0], length=None, color=Color.YELLOW, direction=direction, stop_at_color=[Color.TEAL])

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

    # check if the red and teal pixels are in the same row or column
    # if they are, then try again
    if red_x == teal_x or red_y == teal_y:
        return generate_input()
    
    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)