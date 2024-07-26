from common import *

import numpy as np
from typing import *

# concepts:
# direction, connecting colors, symmetry

# description:
# In the input, you will see a black grid with a green line of connected pixels that extends more than half the height of the grid (either vertically or horizontally).
# The line does not pass through the central point of the grid.
# You should extend the green line by reflecting its path around the central point(s) of the grid upon reaching the boundary or existing line.

def main(input_grid):
    output_grid = input_grid.copy()
    n, m = output_grid.shape
    center_x, center_y = n // 2, m // 2

    # Find the coordinates of the green pixels
    green_pixels = np.argwhere(input_grid == Color.GREEN)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for gx, gy in green_pixels:
        for dx, dy in directions:
            cx, cy = gx + dx, gy + dy
            if 0 <= cx < n and 0 <= cy < m:
                # Reflecting around central point
                if abs(center_x - cx) == abs(center_y - cy):
                    continue
                output_grid[cx, cy] = Color.GREEN
    
    return output_grid

def generate_input():
    # Make a black grid of random dimensions between 10 and 20
    n, m = np.random.randint(10, 21, 2)
    grid = np.full((n, m), Color.BLACK)

    # Choose vertical or horizontal direction randomly
    direction = np.random.choice(['vertical', 'horizontal'])

    if direction == 'vertical':
        # Create a green line that spans more than half of vertically (height)
        length = np.random.randint(n // 2 + 1, n)
        start_y = np.random.randint(0, m)
        for i in range(length):
            grid[i, start_y] = Color.GREEN
    else:
        # Create a green line that spans more than half horizontally (width)
        length = np.random.randint(m // 2 + 1, m)
        start_x = np.random.randint(0, n)
        for i in range(length):
            grid[start_x, i] = Color.GREEN

    return grid