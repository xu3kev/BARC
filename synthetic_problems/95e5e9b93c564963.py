from common import *

import numpy as np
from typing import *

# concepts:
# flood fill, rectangular cells, mirror symmetry

# description:
# The input grid will have two colored regions on the left half of the grid.
# The task is to mirror the shape and color of the colored regions from the left half to the right half.
# The mirroring happens along a vertical central axis of the grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)

    n, m = input_grid.shape
    half_m = m // 2

    for x in range(n):
        for y in range(half_m):
            color = input_grid[x, y]
            if color != Color.BLACK:
                # Copy color to the mirrored position in the right half
                mirrored_y = m - y - 1
                output_grid[x, mirrored_y] = color
                
    return output_grid


def generate_input() -> np.ndarray:
    n = np.random.randint(5, 10)
    m = 2 * np.random.randint(5, 10)  # Ensure even number of columns for symmetry
    grid = np.zeros((n, m), dtype=int)

    # Generate some random colored regions on the left half of the grid
    num_regions = np.random.randint(1, 4)
    for _ in range(num_regions):
        color = np.random.choice(Color.NOT_BLACK)
        region_n = np.random.randint(1, n//2 + 1)
        region_m = np.random.randint(1, m//4 + 1)
        start_x = np.random.randint(0, n - region_n + 1)
        start_y = np.random.randint(0, m//2 - region_m + 1)
        
        for x in range(start_x, start_x + region_n):
            for y in range(start_y, start_y + region_m):
                grid[x, y] = color

    return grid