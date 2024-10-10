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

    blue_pixel_x, blue_pixel_y = np.argwhere(input_grid == Color.BLUE)[0]

    direction = (1, -1)

    while blue_pixel_y > 0:
        stop_x, stop_y = draw_line(input_grid, blue_pixel_x, blue_pixel_y, direction=direction, color=Color.BLUE)
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
