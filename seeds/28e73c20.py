from common import *

import numpy as np
from typing import *


# concepts:
# patterns, repetition

# description:
# In the input you will see a black nxn grid.
# Return a spiral pattern of green pixels starting from the top left corner of the grid going to the right.

def main(input_grid):
    # get the grid size
    n, _ = input_grid.shape

    # start from the top left corner of the grid
    x, y = 0, 0
    input_grid[x, y] = Color.GREEN

    # we define our initial direction as going to the right, which is (1, 0)
    direction = (1, 0)

    # we also make a helper function to turn the direction clockwise
    def turn_clockwise(direction):
        if direction[0] == 0:
            return -direction[1], 0
        return 0, direction[0]
    
    # lastly, create a turn counter to keep track of how many times we have turned consecutively
    turn_counter = 0

    # continue spiralling until we cannot anymore
    while True:
        # if we have turned 4 times consecutively, we break
        if turn_counter == 4:
            break
        
        # first, check if the square after the current one is green, if so, we turn clockwise
        if 0 <= x + 2 * direction[0] < n and 0 <= y + 2 * direction[1] < n and input_grid[x + 2 * direction[0], y + 2 * direction[1]] == Color.GREEN:
            direction = turn_clockwise(direction)
            turn_counter += 1
            continue
        
        # if the next square is not in the grid, we turn clockwise
        if not (0 <= x + direction[0] < n and 0 <= y + direction[1] < n):
            direction = turn_clockwise(direction)
            turn_counter += 1
            continue
        
        # if the next square is not black, we turn clockwise
        if input_grid[x + direction[0], y + direction[1]] != Color.BLACK:
            direction = turn_clockwise(direction)
            turn_counter += 1
            continue
        
        # then we move to the next square and color it green
        x += direction[0]
        y += direction[1]
        input_grid[x, y] = Color.GREEN
        turn_counter = 0

    return input_grid


def generate_input():
    # first create a randomly sized grid, somewhere between 5x5 and 20x20
    n = random.randint(5, 20)
    grid = np.full((n, n), Color.BLACK)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)