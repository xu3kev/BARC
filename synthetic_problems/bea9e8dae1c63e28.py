from common import *

import numpy as np
from typing import *

# concepts:
# direction, lines, intersection

# description:
# In the input grid, you will see several pairs of colored pixels. Each color pair corresponds to two endpoints: one should be the starting point of a vertical line and the other the starting point of a horizontal line.
# The goal is to extend these colored pixels into lines until they hit the edge of the grid.
# If two lines of different colors cross, the intersection point should be marked as black.

def main(input_grid):
    # make output grid
    output_grid = np.copy(input_grid)
    
    # get the indices of all color pixels except black
    non_black_pixels = np.argwhere(input_grid != Color.BLACK)

    # dictionary that keeps track of drawn lines
    horizontal_lines = {}
    vertical_lines = {}

    # Extension lines for all colored pixels
    for x, y in non_black_pixels:
        color = input_grid[x, y]
        if color not in horizontal_lines:
            horizontal_lines[color] = []
        if color not in vertical_lines:
            vertical_lines[color] = []

        # Draw vertical and horizontal lines through the grid until the edges
        vertical_lines[color].append((x, y))
        horizontal_lines[color].append((x, y))

    # Extend vertical lines and intersect them with horizontal lines
    for color, points in vertical_lines.items():
        for point in points:
            x, y = point
            draw_line(output_grid, x, y, length=None, color=color, direction=(0, 1))
            draw_line(output_grid, x, y, length=None, color=color, direction=(0, -1))

    # Extend horizontal lines and intersect them with vertical lines
    intersection_points = set()
    for color, points in horizontal_lines.items():
        for point in points:
            x, y = point
            draw_line(output_grid, x, y, length=None, color=color, direction=(1, 0))
            draw_line(output_grid, x, y, length=None, color=color, direction=(-1, 0))

            # Check intersection with different color lines
            for v_color, v_points in vertical_lines.items():
                if color != v_color:
                    for v_point in v_points:
                        vx, vy = v_point
                        if vx == x and vy < y:
                            for i in range(vy, y + 1):
                                if output_grid[vx, i] == color:
                                    intersection_points.add((vx, i))
                        elif vx == x and vy > y:
                            for i in range(y, vy + 1):
                                if output_grid[vx, i] == color:
                                    intersection_points.add((vx, i))
                        elif vy == y and vx < x:
                            for i in range(vx, x + 1):
                                if output_grid[i, vy] == color:
                                    intersection_points.add((i, vy))
                        elif vy == y and vx > x:
                            for i in range(x, vx + 1):
                                if output_grid[i, vy] == color:
                                    intersection_points.add((i, vy))

    # Mark intersections points as black
    for ix, iy in intersection_points:
        output_grid[ix, iy] = Color.BLACK

    return output_grid

def generate_input():
    # make a grid of random size
    n = random.randint(5, 10)
    m = random.randint(5, 10)
    grid = np.zeros((n, m), dtype=int)

    # choose random number of pairs of colored pixels, but at least 2 pairs
    n_pairs = random.randint(2, 5)

    for _ in range(n_pairs):
        pair_color = random.choice(list(Color.NOT_BLACK))
        
        # Randomly place two pixels of the same color (forming a pair)
        while True:
            x1, y1 = random.randint(0, n - 1), random.randint(0, m - 1)
            x2, y2 = random.randint(0, n - 1), random.randint(0, m - 1)
            if grid[x1, y1] == Color.BLACK and grid[x2, y2] == Color.BLACK and not (x1 == x2 and y1 == y2):
                grid[x1, y1] = pair_color
                grid[x2, y2] = pair_color
                break

    return grid