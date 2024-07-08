from common import *

import numpy as np
from typing import *

# concepts:
# direction, lines, color

# description:
# In the input you will see a red pixel and a yellow pixel.
# To make the output, draw a diagonal yellow line from the red pixel to the yellow pixel.
# If the red and yellow pixels are on the same diagonal, draw the line directly between them.
# If they are not on the same diagonal, choose the shortest diagonal path, then draw the line connecting them.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # find the red and yellow pixels
    red_x, red_y = np.where(input_grid == Color.RED)
    yellow_x, yellow_y = np.where(input_grid == Color.YELLOW)

    # Check if the red and yellow pixel are on the same diagonal
    if abs(red_x[0] - yellow_x[0]) == abs(red_y[0] - yellow_y[0]):
        # draw the direct diagonal line
        direction = ((yellow_x[0] - red_x[0]) // abs(yellow_x[0] - red_x[0]),
                     (yellow_y[0] - red_y[0]) // abs(yellow_y[0] - red_y[0]))
        draw_line(output_grid, red_x[0], red_y[0], length=None, color=Color.YELLOW, direction=direction)
    else:
        # Find the shortest diagonal path to connect them
        while red_x[0] != yellow_x[0] and red_y[0] != yellow_y[0]:
            dx = 1 if yellow_x[0] > red_x[0] else -1
            dy = 1 if yellow_y[0] > red_y[0] else -1
            red_x[0] += dx
            red_y[0] += dy
            output_grid[red_x[0], red_y[0]] = Color.YELLOW

        # If red and yellow pixels are aligned vertically or horizontally
        if red_x[0] == yellow_x[0]:
            direction = (0, 1 if yellow_y[0] > red_y[0] else -1)
        else:  # red_y[0] == yellow_y[0]
            direction = (1 if yellow_x[0] > red_x[0] else -1, 0)

        draw_line(output_grid, red_x[0], red_y[0], length=None, color=Color.YELLOW, direction=direction, stop_at_color=[Color.YELLOW])

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

    # select a random position for the yellow pixel
    yellow_x = np.random.randint(0, n)
    yellow_y = np.random.randint(0, m)
    grid[yellow_x, yellow_y] = Color.YELLOW

    # check if the red and yellow pixels are not in the same position
    # if they are, then try again
    if red_x == yellow_x and red_y == yellow_y:
        return generate_input()
    
    return grid