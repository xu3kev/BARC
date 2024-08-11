from common import *
import numpy as np
from typing import *

# concepts:
# spiral patterns, uniqueness

# description:
# In the input, you will see a grid with a black background and colored pixels sprinkled on it. Exactly one color occurs only one time.
# To make the output, find the cell whose color is unique (color occurs only one time), and create a spiral pattern starting from that cell, with all other cells black.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Plan:
    # 1. Create an output canvas filled with black
    # 2. Find the unique color
    # 3. Create a spiral pattern starting from the unique color cell

    output_grid = np.zeros_like(input_grid)

    # 2. Find the unique color
    unique_color = None
    for color in Color.NOT_BLACK:
        if np.count_nonzero(input_grid == color) == 1:
            unique_color = color
            break
    
    # Find unique cell coordinates
    unique_cell = np.argwhere(input_grid == unique_color)[0]
    x, y = unique_cell

    # 3. Create a spiral pattern
    # Define directions for spiral (right, down, left, up)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_index = 0  # Start direction is 'right'
    step_len = 1  # Initial step length

    output_grid[x, y] = unique_color
    steps = 1  # Number of steps moved in the current direction

    while True:
        dx, dy = directions[dir_index]
        for _ in range(step_len):
            x += dx
            y += dy
            if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
                output_grid[x, y] = unique_color
                steps += 1
            else:
                return output_grid

        dir_index = (dir_index + 1) % 4
        if dir_index % 2 == 0:
            step_len += 1

    return output_grid


def generate_input() -> np.ndarray:
    n, m = 15, 15
    grid = np.zeros((n, m), dtype=int)

    unique_color = random.choice(Color.NOT_BLACK)

    non_border_cells = [ (i, j) for i in range(1, n-1) for j in range(1, m-1) ]
    unique_cell = random.choice(non_border_cells)
    grid[unique_cell] = unique_color

    remaining_colors = [ color for color in Color.NOT_BLACK if color != unique_color ]

    for remaining_color in remaining_colors:
        frequency_of_this_color = random.choice([0, 2, 3, 4, 5, 6])
        for _ in range(frequency_of_this_color):
            empty_cells = [ (i, j) for i in range(n) for j in range(m) if grid[i][j] == Color.BLACK ]
            x, y = random.choice(empty_cells)
            grid[x, y] = remaining_color

    return grid