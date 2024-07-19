from common import *
import numpy as np
from typing import *

# concepts:
# patterns, reflection, growing

# description:
# In the input you will see a grid with multiple randomly-sized and colored concentric circles.
# To make the output, reflect the pattern horizontally and vertically,
# and then grow each circle by one pixel all around its boundary in both the reflected patterns.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Finding the dimensions of the input grid
    h, w = input_grid.shape

    # Reflecting the pattern horizontally
    h_reflection = input_grid[:, ::-1]

    # Reflecting the pattern vertically
    v_reflection = input_grid[::-1, :]

    # Reflecting the pattern both horizontally and vertically
    hv_reflection = input_grid[::-1, ::-1]

    # Concatenating patterns to get a larger grid
    top_half = np.concatenate((input_grid, h_reflection), axis=1)
    bottom_half = np.concatenate((v_reflection, hv_reflection), axis=1)
    output_grid = np.concatenate((top_half, bottom_half), axis=0)

    # Function to grow circles in the grid
    def grow_circle(grid):
        grown_grid = grid.copy()
        h, w = grid.shape
        for x in range(1, h-1):
            for y in range(1, w-1):
                if grid[x, y] != Color.BLACK:
                    grown_grid[x-1:x+2, y-1:y+2] = grid[x, y]
        return grown_grid

    # Growing each circle by one pixel
    output_grid = grow_circle(output_grid)

    return output_grid


def generate_input() -> np.ndarray:
    # Create random concentric circles
    n, m = np.random.randint(10, 15, size=2)
    grid = np.full((n, m), Color.BLACK)

    num_circles = np.random.randint(2, 5)
    cx, cy = n // 2, m // 2

    for _ in range(num_circles):
        radius = np.random.randint(1, min(n, m) // 2)
        color = np.random.choice(list(Color.NOT_BLACK))
        for x in range(n):
            for y in range(m):
                if (cx - x) ** 2 + (cy - y) ** 2 <= radius ** 2:
                    grid[x, y] = color

    return grid