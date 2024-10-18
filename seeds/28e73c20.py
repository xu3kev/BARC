from common import *

import numpy as np
from typing import *

# concepts:
# geometric pattern, repetition, spiral

# description:
# In the input you will see an empty black grid.
# To make the output, you should draw a spiral pattern of green pixels starting from the top left corner and going to the right.

def main(input_grid):
    # get the grid size
    width, height = input_grid.shape

    # start from the top left corner of the grid
    x, y = 0, 0
    output_grid = input_grid.copy()
    output_grid[x, y] = Color.GREEN

    # we define our initial direction as going to the right, which is (1, 0)
    direction = (1, 0)

    # we also make a helper function to turn the direction clockwise
    def turn_clockwise(direction):
        if direction[0] == 0:
            return -direction[1], 0
        return 0, direction[0]

    # continue spiralling until we cannot anymore
    while True:
        # First, check if we hit the border, if so, we turn clockwise
        if x + direction[0] >= width or y + direction[1] >= height or x + direction[0] < 0 or y + direction[1] < 0:
            direction = turn_clockwise(direction)
            continue

        # Then, check if the square after the current one is green, if so,
        # we are already spiralling, so stop here
        if output_grid[x + direction[0], y + direction[1]] == Color.GREEN:
            break

        # Last, check if the square after the current one is green, if so, we turn clockwise
        # We do this to draw the spiral pattern
        if (0 <= x + 2 * direction[0] < width and 0 <= y + 2 * direction[1] < height 
            and output_grid[x + 2 * direction[0], y + 2 * direction[1]] == Color.GREEN):
            direction = turn_clockwise(direction)
            continue
        
        # then we move to the next square and color it green
        x += direction[0]
        y += direction[1]
        output_grid[x, y] = Color.GREEN

    return output_grid

def generate_input():
    # first create a randomly sized grid, somewhere between 5x5 and 20x20
    length = random.randint(5, 20)
    grid = np.full((length, length), Color.BLACK)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)