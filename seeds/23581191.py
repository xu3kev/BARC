from common import *

import numpy as np
from typing import *

# concepts:
# lines, intersection

# description:
# In the input, you will see a grid with a single orange pixel and a single teal pixel.
# To make the output, draw an orange vertical line and an orange horizontal line that intersect at the orange pixel, and draw a teal vertical line and a teal horizontal line that intersect at the teal pixel. The lines should go from edge to edge of the grid.
# Lastly, draw a red pixel where the teal and orange lines intersect.

def main(input_grid):
    # make output grid
    output_grid = np.copy(input_grid)

    # get the index of the orange pixel
    orange = np.where(input_grid == Color.ORANGE)
    x, y = orange[0][0], orange[1][0]

    # get the index of the teal pixel
    teal = np.where(input_grid == Color.TEAL)
    x2, y2 = teal[0][0], teal[1][0]

    # draw lines from one edge of the grid through the orange and teal pixels and across to the other edge of the grid:
    # draw orange vertical line
    output_grid[x, :] = Color.ORANGE # Can also use draw_line(output_grid, x, 0, length=None, color=Color.ORANGE, direction=(0, 1))
    # draw orange horizontal line
    output_grid[:, y] = Color.ORANGE # Can also use draw_line(output_grid, 0, y, length=None, color=Color.ORANGE, direction=(1, 0))
    # draw teal vertical line
    output_grid[x2, :] = Color.TEAL # Can also use draw_line(output_grid, x2, 0, length=None, color=Color.TEAL, direction=(0, 1))
    # draw teal horizontal line
    output_grid[:, y2] = Color.TEAL # Can also use draw_line(output_grid, 0, y2, length=None, color=Color.TEAL, direction=(1, 0))
    

    # draw both intersection points
    output_grid[x, y2] = Color.RED
    output_grid[x2, y] = Color.RED

    return output_grid

def generate_input():
    # make a 9x9 black grid for the background
    n = m = 9
    grid = np.zeros((n,m), dtype=int)

    # put an orange pixel at a random point on the grid
    x, y = np.random.randint(0, n), np.random.randint(0, m)
    grid[x,y] = Color.ORANGE

    # put a teal pixel at a random point on the grid but not in the same row or column as the orange pixel
    x2, y2 = np.random.randint(0, n), np.random.randint(0, m)
    while x2 == x or y2 == y:
        x2, y2 = np.random.randint(0, n), np.random.randint(0, m)
    grid[x2,y2] = Color.TEAL

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)