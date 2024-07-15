from common import *

import numpy as np
from typing import *

def main(input_grid):
    # make the output grid and copy the input into it
    output_grid = np.copy(input_grid)

    # find the coordinates of the single colored pixel
    colors = set(Color.NOT_BLACK)
    for color in colors:
        x, y = np.where(input_grid == color)
        if x.size > 0:
            colored_x = x[0]
            colored_y = y[0]
            pixel_color = color
            break

    # draw vertical line through the colored pixel
    draw_line(output_grid, colored_x, colored_y, length=None, color=pixel_color, direction=(-1, 0))
    draw_line(output_grid, colored_x, colored_y, length=None, color=pixel_color, direction=(1, 0))

    # draw horizontal line through the colored pixel
    draw_line(output_grid, colored_x, colored_y, length=None, color=pixel_color, direction=(0, -1))
    draw_line(output_grid, colored_x, colored_y, length=None, color=pixel_color, direction=(0, 1))

    # draw the border of the grid with the same color
    n, m = input_grid.shape
    draw_line(output_grid, 0, 0, length=m, color=pixel_color, direction=(1, 0))
    draw_line(output_grid, n-1, 0, length=m, color=pixel_color, direction=(1, 0))
    draw_line(output_grid, 0, 0, length=n, color=pixel_color, direction=(0, 1))
    draw_line(output_grid, 0, m-1, length=n, color=pixel_color, direction=(0, 1))

    return output_grid


def generate_input():
    # make a rectangular black grid
    n = np.random.randint(6, 12)
    m = np.random.randint(6, 12)
    grid = np.zeros((n, m), dtype=int)

    # select a random position for a single colored pixel
    x = np.random.randint(1, n-1)
    y = np.random.randint(1, m-1)
    color = np.random.choice(list(Color.NOT_BLACK))
    grid[x, y] = color

    return grid