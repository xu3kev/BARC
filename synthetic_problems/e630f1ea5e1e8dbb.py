from common import *

import numpy as np
from typing import *


# concepts:
# diagonal lines, direction, collision detection

# description:
# In the input, you will see multiple colored pixels on a black background. 
# Each colored pixel will move diagonally in a specific direction (top-left to bottom-right or top-right to bottom-left).
# When they intersect with another colored pixel, they will stop.
# In the output, you'll see two diagonal lines of different colors intersecting at the points where they collided.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # get the coordinates of the non-background pixels
    colored_pixels = np.argwhere(input_grid > 0)
    
    # create two direction vectors for the diagonal movement
    directions = {
        "top_left_to_bottom_right": (1, 1),
        "top_right_to_bottom_left": (1, -1)
    }

    def move_pixel(x, y, direction):
        dx, dy = directions[direction]
        while 0 <= x < input_grid.shape[0] and 0 <= y < input_grid.shape[1]:
            new_x, new_y = x + dx, y + dy
            if new_x < 0 or new_x >= input_grid.shape[0] or new_y < 0 or new_y >= input_grid.shape[1]:
                break
            if output_grid[new_x, new_y] != Color.BLACK:
                break
            output_grid[new_x, new_y] = output_grid[x, y]
            output_grid[x, y] = Color.BLACK
            x, y = new_x, new_y

    for (x, y) in colored_pixels:
        color = input_grid[x, y]
        if x % 2 == 0:
            move_pixel(x, y, "top_left_to_bottom_right")
        else:
            move_pixel(x, y, "top_right_to_bottom_left")

    return output_grid


def generate_input():
    # create a random size grid
    n = m = np.random.randint(5, 20)
    grid = np.zeros((n, m), dtype=int)
    
    # randomly determine the number of colored pixels
    num_pixels = np.random.randint(1, min(n, m) // 2)

    # scatter the colored pixels randomly on the grid
    for _ in range(num_pixels):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        color = np.random.choice(list(Color.NOT_BLACK))
        grid[x, y] = color

    return grid

# This is just a representation of how the functions can be called for testing