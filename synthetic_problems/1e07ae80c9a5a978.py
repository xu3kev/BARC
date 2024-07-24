from common import *

import numpy as np
from typing import *

# concepts:
# array rotation, color detection, constraints

# description:
# You are given a grid with randomly distributed colored pixels. Some of the pixels are marked with BLUE.
# Rotate the grid 90 degrees clockwise while ensuring that the BLUE pixels remain in their original positions.
# Other colored pixels are rotated as per the standard 90-degree rotation rule.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros((m, n), dtype=int)

    # Copy the blue pixels to the new grid
    for x in range(n):
        for y in range(m):
            if input_grid[x, y] == Color.BLUE:
                output_grid[x, y] = Color.BLUE

    # Rotate non-blue pixels 90 degrees clockwise
    for x in range(n):
        for y in range(m):
            if input_grid[x, y] != Color.BLUE:
                new_x = y
                new_y = n - 1 - x
                # Only place non-blue colors in non-blue positions in the output grid
                if output_grid[new_x, new_y] == Color.BLACK:
                    output_grid[new_x, new_y] = input_grid[x, y]

    return output_grid


def generate_input():
    n, m = np.random.randint(5, 15), np.random.randint(5, 15)
    grid = np.full((n, m), Color.BLACK)

    # Randomly populate the grid with some colors
    num_colors = np.random.randint(1, 5, size=(n, m))
    for x in range(n):
        for y in range(m):
            if np.random.random() < 0.2:
                grid[x, y] = np.random.choice([color for color in Color.NOT_BLACK if color != Color.BLUE])

    # Randomly add some BLUE pixels
    for _ in range(np.random.randint(1, 5)):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.BLUE

    return grid