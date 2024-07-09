from common import *

import numpy as np
from typing import *

# concepts:
# lines, color, direction

# description:
# In the input you will see a blue pixel and a green pixel.
# To make the output, draw a diagonal yellow line from the blue pixel towards the green pixel.
# When the line reaches either the same row or column as the green pixel, change the line color to orange and continue to the green pixel.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # find the blue and green pixels
    blue_y, blue_x = np.where(input_grid == Color.BLUE)
    green_y, green_x = np.where(input_grid == Color.GREEN)

    blue_y, blue_x = blue_y[0], blue_x[0]
    green_y, green_x = green_y[0], green_x[0]

    # determine the direction of the diagonal line
    dx = 1 if green_x > blue_x else -1
    dy = 1 if green_y > blue_y else -1

    # draw the diagonal yellow line
    x, y = blue_x, blue_y
    while x != green_x and y != green_y:
        x += dx
        y += dy
        if output_grid[y, x] == Color.BLACK:
            output_grid[y, x] = Color.YELLOW

    # draw the remaining part of the line in orange
    if x == green_x:
        # vertical line needed
        draw_line(output_grid, x, y, length=None, color=Color.ORANGE, direction=(0, dy), stop_at_color=[Color.GREEN])
    else:
        # horizontal line needed
        draw_line(output_grid, x, y, length=None, color=Color.ORANGE, direction=(dx, 0), stop_at_color=[Color.GREEN])

    return output_grid


def generate_input():
    # make a black grid as the background
    n = np.random.randint(8, 20)
    m = np.random.randint(8, 20)
    grid = np.zeros((n, m), dtype=int)

    # select a random position for the blue pixel
    blue_y = np.random.randint(0, n)
    blue_x = np.random.randint(0, m)
    grid[blue_y, blue_x] = Color.BLUE

    # select a random position for the green pixel
    green_y = np.random.randint(0, n)
    green_x = np.random.randint(0, m)
    grid[green_y, green_x] = Color.GREEN

    # check if the blue and green pixels are in the same row and column
    # if they are, then try again
    if blue_y == green_y and blue_x == green_x:
        return generate_input()
    
    return grid