from common import *
import numpy as np
from typing import *

# concepts:
# symmetry, diagonal lines, reflection

# description:
# In the input grid you will see two colored pixels of the same color on a black background, symmetrically placed around the center of the grid.
# To make the output, draw diagonal lines connecting these two pixels, and then reflect this pattern across both axes (horizontal and vertical) to achieve a symmetrical pattern.

def main(input_grid):
    # make output grid
    output_grid = np.copy(input_grid)

    # get the indices of the colored pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    assert len(colored_pixels) == 2

    # get color from the colored pixel
    color = input_grid[colored_pixels[0][0], colored_pixels[0][1]]

    # draw diagonals connecting the two colored pixels
    draw_line(output_grid, colored_pixels[0][0], colored_pixels[0][1], length=None, color=color, direction=(1, 1))
    draw_line(output_grid, colored_pixels[1][0], colored_pixels[1][1], length=None, color=color, direction=(-1, -1))
    draw_line(output_grid, colored_pixels[0][0], colored_pixels[0][1], length=None, color=color, direction=(-1, -1))
    draw_line(output_grid, colored_pixels[1][0], colored_pixels[1][1], length=None, color=color, direction=(1, 1))

    # horizontally reflect
    output_grid = np.concatenate((output_grid, output_grid[:, ::-1]), axis=1)
    # vertically reflect
    output_grid = np.concatenate((output_grid, output_grid[::-1, :]), axis=0)

    return output_grid

def generate_input():
    # make a square black grid for the background first
    n = np.random.randint(5, 20)
    grid = np.zeros((n, n), dtype=int)

    # put two symmetrically placed, randomly colored pixels on the grid
    color = np.random.choice(list(Color.NOT_BLACK))
    center_x, center_y = n // 2, n // 2

    offset = np.random.randint(1, n // 2)
    grid[center_x - offset, center_y - offset] = color
    grid[center_x + offset, center_y + offset] = color

    return grid