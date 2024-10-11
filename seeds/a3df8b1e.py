from common import *

import numpy as np
from typing import *

# concepts:
# bouncing

# description:
# In the input you will see a single blue pixel on a black background
# To make the output, shoot the blue pixel diagonally up and to the right, having it reflect and bounce off the walls until it exits at the top of the grid

def main(input_grid):
    # Plan:
    # 1. Detect the pixel
    # 2. Shoot each line of the reflection one-by-one, bouncing (changing horizontal direction) when it hits a (horizontal) wall/edge of canvas

    # 1. Find the location of the pixel
    objects = find_connected_components(input_grid, connectivity=4, background=Color.BLACK)
    assert len(objects) == 1, "There should be exactly one blue pixel"
    blue_pixel = list(objects)[0]
    blue_pixel_x, blue_pixel_y = object_position(blue_pixel, background=Color.BLACK, anchor='center')

    # 2. do the bounce which requires keeping track of the direction of the ray we are shooting, as well as the tip of the ray
    # initially we are shooting diagonally up and to the right (dx=1, dy=-1)
    # initially the tip of the ray is the blue pixel, x=blue_pixel_x, y=blue_pixel_y
    direction = (1, -1)

    # loop until we fall out of the canvas
    while 0 <= blue_pixel_x < input_grid.shape[0] and 0 <= blue_pixel_y < input_grid.shape[1]:
        stop_x, stop_y = draw_line(input_grid, blue_pixel_x, blue_pixel_y, direction=direction, color=Color.BLUE)
        # Terminate if we failed to make progress
        if stop_x == blue_pixel_x and stop_y == blue_pixel_y:
            break
        blue_pixel_x, blue_pixel_y = stop_x, stop_y
        direction = (-direction[0], direction[1])
    
    return input_grid


def generate_input():
    width, height = np.random.randint(2, 15), np.random.randint(10, 30)
    grid = np.full((width, height), Color.BLACK)
    grid[0,-1] = Color.BLUE

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
