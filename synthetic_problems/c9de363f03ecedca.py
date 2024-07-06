from common import *

import numpy as np
from typing import *

# concepts:
# symmetric extension, pixel manipulation

# description:
# In the input, you will see a grid with some colored pixels.
# To create the output:
# 1. Identify the center of the grid.
# 2. Reflect each colored pixel across the vertical axis passing through the center.
# 3. Reflect each colored pixel across the horizontal axis passing through the center.
# 4. Finally, reflect each colored pixel across both axes.
# 5. The output grid should be double the size of the input grid in both dimensions.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.full((2 * n, 2 * m), Color.BLACK)

    # Reflect pixels across the vertical axis passing through the center
    for x in range(n):
        for y in range(m):
            color = input_grid[x, y]
            if color != Color.BLACK:
                output_grid[x, y] = color  # Original
                output_grid[x, 2 * m - y - 1] = color  # Horizontal reflection
                output_grid[2 * n - x - 1, y] = color  # Vertical reflection
                output_grid[2 * n - x - 1, 2 * m - y - 1] = color  # Both axes reflection

    return output_grid

def generate_input():
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)
    grid = np.full((n, m), Color.BLACK)
    
    num_pixels = np.random.randint(1, min(n, m) + 1)

    for _ in range(num_pixels):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        color = np.random.choice(list(Color.NOT_BLACK))
        grid[x, y] = color

    return grid