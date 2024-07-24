from common import *

import numpy as np
from typing import *

# concepts:
# connectivity, intersection, lines, growing

# description:
# Given an input grid with some one-pixel colored stars on a black background.
# Each colored star grows into intersecting diagonal lines until they touch another star or the edge of the grid.
# The points of intersection between the lines will be filled with a new color (e.g., red).

def main(input_grid):
    # Get the positions of the colored stars and their corresponding colors
    stars = np.argwhere(input_grid != Color.BLACK)
    star_colors = input_grid[stars[:, 0], stars[:, 1]]

    output_grid = np.copy(input_grid)
    intersections = []

    def is_valid_position(x, y):
        return 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]

    def grow_star(x, y, color):
        # Grow diagonally in four directions until an intersection or the edge of the grid
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            cx, cy = x, y
            while is_valid_position(cx + dx, cy + dy):
                cx += dx
                cy += dy
                # If we hit another color or an intersection point
                if output_grid[cx, cy] != Color.BLACK:
                    intersections.append((cx, cy))
                    break
                output_grid[cx, cy] = color

    for (x, y), color in zip(stars, star_colors):
        grow_star(x, y, color)
    
    # Mark intersections with red
    for ix, iy in intersections:
        output_grid[ix, iy] = Color.RED
    
    return output_grid

def generate_input():
    # Randomly generate a grid size between 10x10 to 15x15
    n, m = np.random.randint(10, 16), np.random.randint(10, 16)
    grid = np.zeros((n, m), dtype=int)

    # Randomly place 3 to 5 stars of random colors on the grid
    num_stars = np.random.randint(3, 6)
    colors = list(Color.NOT_BLACK)
    
    for _ in range(num_stars):
        color = np.random.choice(colors)
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        while grid[x, y] != Color.BLACK:
            x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = color

    return grid