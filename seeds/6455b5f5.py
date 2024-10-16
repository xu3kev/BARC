from common import *

import numpy as np
from typing import *

# concepts:
# filling

# description:
# The input consists of a black grid. The grid is divided with red lines into black rectangles of different sizes.
# To produce the output grid, fill in the smallest black rectangles with teal, and fillin in the largest black rectangles with blue.

def main(input_grid):
    # to get the black rectangles, find connected components with red as background
    objects = find_connected_components(input_grid, background=Color.RED, connectivity=4, monochromatic=True)

    # get object areas
    object_areas = [np.sum(obj == Color.BLACK) for obj in objects]

    # find the smallest and largest areas
    smallest_area = min(object_areas)
    largest_area = max(object_areas)

    # fill in the smallest rectangles with teal, and the largest rectangles with blue
    new_objects = []
    for obj in objects:
        area = np.sum(obj == Color.BLACK)
        if area == smallest_area:
            obj[obj == Color.BLACK] = Color.TEAL
        elif area == largest_area:
            obj[obj == Color.BLACK] = Color.BLUE
        new_objects.append(obj)

    # create an output grid to store the result
    output_grid = np.full(input_grid.shape, Color.RED)

    # blit the objects back into the grid
    for obj in new_objects:
        blit_object(output_grid, obj, background=Color.RED)

    return output_grid


def generate_input():
    # create a grid of size 10-20x10-20
    n = np.random.randint(10, 21)
    m = np.random.randint(10, 21)
    grid = np.full((n, m), Color.BLACK)

    num_lines = np.random.randint(3, 15)

    for i in range(num_lines):
        # add a red line to divide the grid somewhere
        x, y = np.random.randint(2, n-1), np.random.randint(2, m-1)
        # make sure we're not neighboring a red line already
        if Color.RED in [grid[x, y+1], grid[x, y-1], grid[x+1, y], grid[x-1, y]]:
            continue

        horizontal = np.random.choice([True, False])
        if horizontal:
            draw_line(grid, x, y, direction=(1, 0), color=Color.RED, stop_at_color=[Color.RED])
            draw_line(grid, x-1, y, direction=(-1, 0), color=Color.RED, stop_at_color=[Color.RED])
        else:
            draw_line(grid, x, y, direction=(0, 1), color=Color.RED, stop_at_color=[Color.RED])
            draw_line(grid, x, y-1, direction=(0, -1), color=Color.RED, stop_at_color=[Color.RED])

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)

