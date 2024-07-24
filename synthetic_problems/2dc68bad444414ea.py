from common import *

import numpy as np
from typing import *

# concepts: radial expansion, pixel dilation
# description: 
# In the input, you will see a grid with some non-black pixels scattered around.
# The output will expand each non-black pixel radially outward by a fixed number of steps.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    expansion_steps = 2  # fixed number of steps for radial expansion

    # Get the coordinates of all non-black pixels
    non_black_indices = np.argwhere(input_grid != Color.BLACK)

    for x, y in non_black_indices:
        origin_color = input_grid[x, y]
        # Expand radially from the non-black pixel
        for dx in range(-expansion_steps, expansion_steps + 1):
            for dy in range(-expansion_steps, expansion_steps + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < output_grid.shape[0] and 0 <= ny < output_grid.shape[1]:
                    output_grid[nx, ny] = origin_color
    
    return output_grid

def generate_input():
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    num_non_black_pixels = np.random.randint(3, 8)
    used_positions = set()
    for _ in range(num_non_black_pixels):
        while True:
            x, y = np.random.randint(0, n), np.random.randint(0, m)
            if (x, y) not in used_positions:
                used_positions.add((x, y))
                grid[x, y] = np.random.choice(list(Color.NOT_BLACK))
                break
                
    return grid