from common import *

import numpy as np
from typing import *

# concepts:
# reflection, connecting colors, repeating pattern

# description:
# In the input grid, you will see a central rectangular border of a random color.
# Reflect this border diagonally to generate four quadrants.
# In each quadrant, extend this border outward by two cells at a time until the entire grid is filled.

def main(input_grid):
    def in_bounds(grid, x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def draw_extended_border(grid, top_left_x, top_left_y, w, h, color):
        for dx in range(w + 1):
            if in_bounds(grid, top_left_x + dx, top_left_y):
                grid[top_left_x + dx, top_left_y] = color
            if in_bounds(grid, top_left_x + dx, top_left_y + h):
                grid[top_left_x + dx, top_left_y + h] = color
        for dy in range(h + 1):
            if in_bounds(grid, top_left_x, top_left_y + dy):
                grid[top_left_x, top_left_y + dy] = color
            if in_bounds(grid, top_left_x + w, top_left_y + dy):
                grid[top_left_x + w, top_left_y + dy] = color

    center_x, center_y = input_grid.shape[0] // 2, input_grid.shape[1] // 2
    top_left_x, top_left_y = center_x - 2, center_y - 2
    width, height = 4, 4

    color = input_grid[top_left_x + 1, top_left_y + 1]

    output_grid = input_grid.copy()

    patterns = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dx, dy in patterns:
        i = 1
        while True:
            old_grid = output_grid.copy()
            draw_extended_border(output_grid, center_x + dx * width * i, center_y + dy * height * i, width * i, height * i, color)
            if np.array_equal(old_grid, output_grid):
                break
            i += 2

    return output_grid

def generate_input():
    size = np.random.randint(12, 20)
    input_grid = np.full((size, size), Color.BLACK)

    color = np.random.choice(Color.NOT_BLACK)
    center_x, center_y = size // 2, size // 2
    top_left_x, top_left_y = center_x - 2, center_y - 2
    width, height = 4, 4

    for dx in range(width + 1):
        input_grid[top_left_x + dx, top_left_y] = color
        input_grid[top_left_x + dx, top_left_y + height] = color
    for dy in range(height + 1):
        input_grid[top_left_x, top_left_y + dy] = color
        input_grid[top_left_x + width, top_left_y + dy] = color

    return input_grid