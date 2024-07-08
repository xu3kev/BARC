from common import *

import numpy as np
from typing import *

# concepts:
# pixel manipulation, growing, Coloring diagonal pixels

# description:
# In the input you will see a medium-sized grid with colored pixels scattered around, including some special ones.
# To make the output:
# 1. For each red pixel, grow it by replicating its color in the diagonal neighbors (northeast, northwest, southeast, southwest) 
#      if the neighbor is either black or green.
# 2. For each blue pixel, grow it by replicating its color in the cardinal neighbors (up, down, left, right) 
#      if the neighbor is either black or yellow.
# 3. No other pixel colors will cause a change.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)

    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            color = input_grid[x][y]
            if color == Color.RED:
                # grow red pixels in diagonal direction if diagonal neighbor is black or green
                for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < input_grid.shape[0] and 0 <= ny < input_grid.shape[1]:
                        if output_grid[nx, ny] in [Color.BLACK, Color.GREEN]:
                            output_grid[nx, ny] = Color.RED
            elif color == Color.BLUE:
                # grow blue pixels in cardinal direction if neighbor is black or yellow
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < input_grid.shape[0] and 0 <= ny < input_grid.shape[1]:
                        if output_grid[nx, ny] in [Color.BLACK, Color.YELLOW]:
                            output_grid[nx, ny] = Color.BLUE

    return output_grid


def generate_input() -> np.ndarray:
    n, m = np.random.randint(5, 20), np.random.randint(5, 20)
    grid = np.zeros((n, m), dtype=int)

    num_red, num_blue, num_green, num_yellow = (
        np.random.randint(1, 5),
        np.random.randint(1, 5),
        np.random.randint(1, 5),
        np.random.randint(1, 5),
    )

    for _ in range(num_red):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.RED

    for _ in range(num_blue):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.BLUE

    for _ in range(num_green):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.GREEN

    for _ in range(num_yellow):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.YELLOW

    return grid