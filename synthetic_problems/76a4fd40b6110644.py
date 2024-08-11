from common import *

import numpy as np
from typing import *

# concepts:
# lines, intersection, patterns

# description:
# In the input, you will see a grid with a single orange pixel, a single teal pixel, and a single green pixel.
# To make the output, draw an orange vertical line and a horizontal line that intersect at the orange pixel, and draw a teal vertical line and horizontal line that intersect at the teal pixel. Similarly, draw green lines intersecting at the green pixel.
# The lines should go from edge to edge of the grid. Finally, at the intersections of these six lines, draw a 3x3 pattern of blue dots, except where the primary colored lines intersect the cells.
# If an intersection does not exist within the grid, ignore drawing the pattern at that intersection.

def main(input_grid):
    # make output grid
    output_grid = np.copy(input_grid)

    # get the index of the orange pixel
    orange = np.where(input_grid == Color.ORANGE)
    x_o, y_o = orange[0][0], orange[1][0]

    # get the index of the teal pixel
    teal = np.where(input_grid == Color.TEAL)
    x_t, y_t = teal[0][0], teal[1][0]

    # get the index of the green pixel
    green = np.where(input_grid == Color.GREEN)
    x_g, y_g = green[0][0], green[1][0]

    # draw lines for orange, teal, and green pixels
    for (x, y, color) in [(x_o, y_o, Color.ORANGE), (x_t, y_t, Color.TEAL), (x_g, y_g, Color.GREEN)]:
        output_grid[x, :] = color
        output_grid[:, y] = color
    
    intersections = [
        (x_o, y_t), (x_o, y_g), (x_t, y_o), (x_t, y_g), (x_g, y_o), (x_g, y_t)
    ]
    
    # Draw 3x3 blue dot pattern around intersection points
    for ix, iy in intersections:
        if 1 <= ix < input_grid.shape[0] - 1 and 1 <= iy < input_grid.shape[1] - 1:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if output_grid[ix + dx, iy + dy] == Color.BLACK:
                        output_grid[ix + dx, iy + dy] = Color.BLUE

    return output_grid

def generate_input():
    # make a 10x10 black grid for the background
    n = m = 10
    grid = np.zeros((n, m), dtype=int)

    # place an orange pixel at a random location
    x_o, y_o = np.random.randint(1, n-1), np.random.randint(1, m-1)
    grid[x_o, y_o] = Color.ORANGE
    
    # place a teal pixel at a random location but not in the same row or column as the orange pixel
    x_t, y_t = np.random.randint(1, n-1), np.random.randint(1, m-1)
    while x_t == x_o or y_t == y_o:
        x_t, y_t = np.random.randint(1, n-1), np.random.randint(1, m-1)
    grid[x_t, y_t] = Color.TEAL
    
    # place a green pixel at a random location but not in the same row or column as the orange and teal pixels
    x_g, y_g = np.random.randint(1, n-1), np.random.randint(1, m-1)
    while x_g == x_o or y_g == y_o or x_g == x_t or y_g == y_t:
        x_g, y_g = np.random.randint(1, n-1), np.random.randint(1, m-1)
    grid[x_g, y_g] = Color.GREEN

    return grid