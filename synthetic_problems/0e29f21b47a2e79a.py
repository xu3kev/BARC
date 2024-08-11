from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines, color, alignment, repetition

# description:
# In the input, you will see a grid consisting of two diagonal lines that intersect at one point.
# Each diagonal line is a different color.
# Extend each pixel that is part of a diagonal line to create a full diagonal from that point to the grid edge in both directions.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)
    input_colors = set(color for row in input_grid for color in row if color != Color.BLACK)

    def extend_diagonal(grid, x, y, color):
        draw_line(grid, x, y, length=None, color=color, direction=(1, 1))
        draw_line(grid, x, y, length=None, color=color, direction=(-1, -1))
        draw_line(grid, x, y, length=None, color=color, direction=(1, -1))
        draw_line(grid, x, y, length=None, color=color, direction=(-1, 1))

    for i in range(n):
        for j in range(m):
            if input_grid[i, j] in input_colors:
                extend_diagonal(output_grid, i, j, input_grid[i, j])

    return output_grid

def generate_input():
    n = np.random.randint(6, 15)
    m = np.random.randint(6, 15)
    grid = np.zeros((n, m), dtype=int)
    color1, color2 = np.random.choice(list(Color.NOT_BLACK), 2, replace=False)
    
    # Random start position for each diagonal line
    start_x1, start_y1 = np.random.randint(0, n), np.random.randint(0, m)
    start_x2, start_y2 = np.random.randint(0, n), np.random.randint(0, m)
    
    draw_line(grid, start_x1, start_y1, length=None, color=color1, direction=(1, 1))
    draw_line(grid, start_x1, start_y1, length=None, color=color1, direction=(-1, -1))
    draw_line(grid, start_x2, start_y2, length=None, color=color2, direction=(1, -1))
    draw_line(grid, start_x2, start_y2, length=None, color=color2, direction=(-1, 1))

    return grid