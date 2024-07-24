from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines, pixel manipulation, color

# description:
# In the input, you will see a grid with some red and blue pixels.
# To make the output:
# 1. For each red pixel, extend diagonal lines of yellow pixels in both directions (i.e., northwest to southeast and northeast to southwest) until the edge of the grid is reached.
# 2. For each blue pixel, extend horizontal lines of orange pixels in both directions (i.e., left to right and right to left) until the edge of the grid is reached.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)

    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            color = input_grid[x][y]

            if color == Color.RED:
                # Extend diagonal lines of yellow pixels in both directions
                draw_line(output_grid, x, y, length=None, color=Color.YELLOW, direction=(1, 1))
                draw_line(output_grid, x, y, length=None, color=Color.YELLOW, direction=(-1, -1))
                draw_line(output_grid, x, y, length=None, color=Color.YELLOW, direction=(1, -1))
                draw_line(output_grid, x, y, length=None, color=Color.YELLOW, direction=(-1, 1))

            elif color == Color.BLUE:
                # Extend horizontal lines of orange pixels in both directions
                draw_line(output_grid, x, y, length=None, color=Color.ORANGE, direction=(0, 1))
                draw_line(output_grid, x, y, length=None, color=Color.ORANGE, direction=(0, -1))
                    
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
        grid[x, y] = np.random.choice([color for color in Color.NOT_BLACK if color not in [Color.RED, Color.BLUE]])

    return grid