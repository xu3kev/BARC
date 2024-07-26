from common import *

import numpy as np
from typing import *

# concepts:
# pattern recognition, diagonal lines, color connection

# description:
# In the input, you will see an 8x8 grid with multiple diagonal lines, each made of two different colors.
# The lines start at the top-left corner of the grid and extend toward the bottom-right corner.
# For each diagonal line, replace it with a checkerboard pattern of its two colors.
# The checkerboard pattern should start from the top-left of the diagonal line and extend outwards.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    
    def apply_checkerboard(grid, x, y, length, c1, c2):
        for i in range(length):
            if x + i < grid.shape[0] and y + i < grid.shape[1]:
                if (i % 2) == 0:
                    grid[x + i, y + i] = c1
                else:
                    grid[x + i, y + i] = c2

    colors_used = set()
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != Color.BLACK and (i, j) not in colors_used:
                length = 0
                c1 = input_grid[i, j]
                x, y = i, j
                while x < input_grid.shape[0] and y < input_grid.shape[1] and input_grid[x, y] != Color.BLACK:
                    colors_used.add((x, y))
                    x += 1
                    y += 1
                    length += 1
                    if input_grid[x-1, y-1] != c1 and input_grid[x-1, y-1] != Color.BLACK:
                        c2 = input_grid[x-1, y-1]
                apply_checkerboard(output_grid, i, j, length, c1, c2)

    return output_grid

def generate_input() -> np.ndarray:
    input_grid = np.full((8, 8), Color.BLACK)
    
    def draw_diagonal(col1, col2, start_x, start_y, length):
        x, y = start_x, start_y
        for _ in range(length):
            if x < 8 and y < 8:
                input_grid[x, y] = col1 if (x + y) % 2 == 0 else col2
                x += 1
                y += 1
          
    num_lines = np.random.randint(3, 6)
    for _ in range(num_lines):
        col1, col2 = np.random.choice(Color.NOT_BLACK, 2, replace=False)
        start_x = np.random.randint(0, 2)
        start_y = np.random.randint(0, 2)
        length = np.random.randint(3, 9 - max(start_x, start_y))
        draw_diagonal(col1, col2, start_x, start_y, length)

    return input_grid