from common import *

import numpy as np
from typing import *

# concepts:
# lines, intersection, symmetry detection

# description:
# In the input, you will see a grid with two colored pixels: one blue and one green.
# To make the output:
# 1. Draw blue horizontal and vertical lines through the blue pixel, extending to the edges of the grid.
# 2. Draw green horizontal and vertical lines through the green pixel, extending to the edges of the grid.
# 3. Find the center point between the blue and green pixels.
# 4. Draw red diagonal lines through this center point, extending from corner to corner of the grid.
# 5. Where any lines intersect (including with the diagonal lines), place a yellow pixel.
# 6. If the center point has rotational symmetry (i.e., it's exactly in the middle of the grid), 
#    fill the four corners of the grid with pink pixels.

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.full((n, m), Color.BLACK)

    # Find blue and green pixels
    blue_coords = np.argwhere(input_grid == Color.BLUE)[0]
    green_coords = np.argwhere(input_grid == Color.GREEN)[0]

    # Draw blue lines
    output_grid[blue_coords[0], :] = Color.BLUE
    output_grid[:, blue_coords[1]] = Color.BLUE

    # Draw green lines
    output_grid[green_coords[0], :] = Color.GREEN
    output_grid[:, green_coords[1]] = Color.GREEN

    # Find center point
    center_x = (blue_coords[0] + green_coords[0]) // 2
    center_y = (blue_coords[1] + green_coords[1]) // 2

    # Draw red diagonal lines
    for i in range(n):
        output_grid[i, i] = Color.RED
        output_grid[i, n-1-i] = Color.RED

    # Mark intersections with yellow
    for i in range(n):
        for j in range(m):
            if np.sum(output_grid[i, j] != Color.BLACK) > 1:
                output_grid[i, j] = Color.YELLOW

    # Check for rotational symmetry and fill corners if symmetric
    if center_x == n // 2 and center_y == m // 2:
        output_grid[0, 0] = Color.PINK
        output_grid[0, m-1] = Color.PINK
        output_grid[n-1, 0] = Color.PINK
        output_grid[n-1, m-1] = Color.PINK

    return output_grid

def generate_input():
    n = m = 9
    grid = np.full((n, m), Color.BLACK)

    # Place blue pixel
    blue_x, blue_y = np.random.randint(0, n), np.random.randint(0, m)
    grid[blue_x, blue_y] = Color.BLUE

    # Place green pixel (not in the same row or column as blue)
    while True:
        green_x, green_y = np.random.randint(0, n), np.random.randint(0, m)
        if green_x != blue_x and green_y != blue_y:
            grid[green_x, green_y] = Color.GREEN
            break

    return grid