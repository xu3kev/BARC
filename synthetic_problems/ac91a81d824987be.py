from common import *

import numpy as np
import random

# concepts:
# spiral patterns

# description:
# In the input, you will see one colored pixel on a black background.
# To make the output, create a spiral pattern from the colored pixel until the boundary of the grid is reached.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.copy(input_grid)

    # locate the colored pixel
    x, y, width, height = bounding_box(input_grid != Color.BLACK)
    color = input_grid[x, y]

    # direction vectors for right, down, left, and up movements
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # current position and direction
    cur_x, cur_y = x, y
    direction_index = 0
    steps_in_current_direction = 1
    steps_taken = 0
    
    while True:
        # move in the current direction
        dx, dy = directions[direction_index]
        cur_x += dx
        cur_y += dy
        steps_taken += 1

        # if the move is out of bounds, we are done
        if not (0 <= cur_x < n and 0 <= cur_y < m):
            break

        # color the current position
        output_grid[cur_x, cur_y] = color

        # after taking the prescribed number of steps, change direction
        if steps_taken == steps_in_current_direction:
            direction_index = (direction_index + 1) % 4
            steps_taken = 0
            
            # after every two turns, increment the steps in current direction
            if direction_index % 2 == 0:
                steps_in_current_direction += 1

    return output_grid

def generate_input():
    # create a black grid of random size
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # place a single colored pixel at a random position
    color = random.choice(list(Color.NOT_BLACK))
    x, y = np.random.randint(0, n-1), np.random.randint(0, m-1)
    grid[x, y] = color

    return grid