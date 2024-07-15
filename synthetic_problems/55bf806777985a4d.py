from common import *

import numpy as np
from typing import *

# concepts:
# Grid mirroring, scaling, proximity, color change

# description:
# In the input you will see a nxm grid with colored pixels scattered throughout,
# and black pixels making a vertical or horizontal line of symmetry.
# For the output, reflect the colored pixels across the line of symmetry and scale the output grid by 2x.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros((2 * n, 2 * m), dtype=int)
    
    # Identify the line of symmetry
    vertical_symmetry = np.all(input_grid[:, m // 2] == Color.BLACK)
    horizontal_symmetry = np.all(input_grid[n // 2, :] == Color.BLACK)
    
    if vertical_symmetry:
        midpoint = m // 2
        for x in range(n):
            for y in range(m):
                if input_grid[x, y] != Color.BLACK:
                    output_grid[2 * x, 2 * y] = input_grid[x, y]
                    output_grid[2 * x, 2 * (2 * midpoint - y)] = input_grid[x, y]
    elif horizontal_symmetry:
        midpoint = n // 2
        for x in range(n):
            for y in range(m):
                if input_grid[x, y] != Color.BLACK:
                    output_grid[2 * x, 2 * y] = input_grid[x, y]
                    output_grid[2 * (2 * midpoint - x), 2 * y] = input_grid[x, y]

    return output_grid


def generate_input():
    # Create a black grid as the background
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)
    grid = np.zeros((n, m), dtype=int)

    # Randomly sprinkle colored pixels
    for _ in range(np.random.randint(5, 15)):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = np.random.choice(list(Color.NOT_BLACK))

    # Decide and draw the line of symmetry
    if np.random.rand() < 0.5:
        # Vertical line of symmetry in the middle
        midpoint = m // 2
        grid[:, midpoint] = Color.BLACK
    else:
        # Horizontal line of symmetry in the middle
        midpoint = n // 2
        grid[midpoint, :] = Color.BLACK

    return grid