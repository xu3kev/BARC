from common import *

import numpy as np
from typing import *

# concepts:
# objects, flood fill, connectivity

# description:
# In the input, you will see a black grid with a red line that starts in the top left corner and bounces off the borders of the grid until it reaches the right side of the grid.
# To make the output, find the black regions separated by the red lines, then, starting with the first region from the left, color every third region yellow.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # find the black regions in the input grid
    black_regions = find_connected_components(input_grid, connectivity=4, background=Color.RED)

    # sort the regions from left to right using the coordinates of their bounding boxes
    black_regions = sorted(black_regions, key=lambda region: bounding_box(region, background=Color.RED)[0])

    # color every third black region yellow using flood fill
    for i, region in enumerate(black_regions):
        if i % 3 == 0:
            x, y = np.where(region == Color.BLACK)
            flood_fill(output_grid, x[0], y[0], Color.YELLOW)

    return output_grid



def generate_input():
    # make a black grid that is 3 cells tall and between 10 and 20 cells wide
    grid = np.zeros((np.random.randint(10,20), 3), dtype=int)

    # make a red line that starts in the top left corner and bounces off the borders of the grid until it reaches the right side of the grid
    x, y = 0, 0
    dx, dy = 1, 1
    # go until we reach the right side of the grid
    while x < grid.shape[0]:
        # make the current cell red
        grid[x, y] = Color.RED
        # if we are at the top or bottom of the grid, bounce off the top or bottom border
        if y + dy >= grid.shape[1]:
            dy = -1
        elif y + dy < 0:
            dy = 1
        x += dx
        y += dy

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
