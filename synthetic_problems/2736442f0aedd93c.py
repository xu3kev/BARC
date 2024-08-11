from common import *

import numpy as np
from typing import *

# concepts:
# extending, diagonal lines, point propagation, connectedness

# description:
# The input is a grid with random colored pixels.
# The transformation extends each pixel's color diagonally (in all four diagonal directions) until it hits the boundary of the grid or another colored pixel.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = input_grid.copy()
    
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    def extend_diagonal(x, y, color):
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < n and 0 <= ny < m and output_grid[nx, ny] == Color.BLACK:
                output_grid[nx, ny] = color
                nx += dx
                ny += dy

    for x in range(n):
        for y in range(m):
            color = input_grid[x, y]
            if color != Color.BLACK:
                extend_diagonal(x, y, color)

    return output_grid

def generate_input():
    n = m = 10  # Grid size
    grid = np.full((n, m), Color.BLACK)  # Initialize with black background
    pixel_count = random.randint(5, 10)  # Random number of colored pixels

    for _ in range(pixel_count):
        x = random.randint(0, n - 1)
        y = random.randint(0, m - 1)
        color = random.choice(list(Color.NOT_BLACK))
        grid[x, y] = color

    return grid