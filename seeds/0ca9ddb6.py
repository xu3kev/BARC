from common import *

import numpy as np
from typing import *

# concepts:
# pixel manipulation

# description:
# In the input you will see a medium sized grid width individual colored pixels, some of which are red or blue (those ones are special)
# To make the output:
# 1. For each red pixel, add yellow pixels in its immediate diagonals (northeast, northwest, southeast, southwest)
# 2. For each blue pixel, add orange pixels in its immediate neighbors (up, down, left, right)

def main(input_grid: np.ndarray) -> np.ndarray:

    output_grid = np.copy(input_grid)

    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            color = input_grid[x][y]
            if color == Color.RED:
                # put yellow pixels in the diagonals
                for dx in [-1, 1]:
                    for dy in [-1, 1]:
                        if 0 <= x+dx < input_grid.shape[0] and 0 <= y+dy < input_grid.shape[1]:
                            output_grid[x+dx, y+dy] = Color.YELLOW
            elif color == Color.BLUE:
                # put orange pixels in the neighbors
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    if 0 <= x+dx < input_grid.shape[0] and 0 <= y+dy < input_grid.shape[1]:
                        output_grid[x+dx, y+dy] = Color.ORANGE

    return output_grid



def generate_input() -> np.ndarray:
    n, m = np.random.randint(5, 20), np.random.randint(5, 20)
    grid = np.zeros((n, m), dtype=int)

    num_red, num_blue, num_other = np.random.randint(1, 5), np.random.randint(1, 5), np.random.randint(1, 5)

    for _ in range(num_red):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.RED
    
    for _ in range(num_blue):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.BLUE
    
    for _ in range(num_other):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = np.random.choice([ color for color in Color.NOT_BLACK if color not in [Color.RED, Color.BLUE] ])


    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main, 5)