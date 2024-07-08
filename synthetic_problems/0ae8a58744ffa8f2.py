import numpy as np
from typing import *
from common import *

# concepts:
# rectangular cells, color guide, boolean logical operations, bitmasks with separator

# description:
# In the input, you will see two grey bars forming four quadrants. Each quadrant contains a bitmask where cells are either blue or black.
# To create the output, color red the cells that are set (blue) in at least three of the four quadrants.


def main(input_grid: np.ndarray) -> np.ndarray:
    # Identify the positions of the vertical and horizontal bars
    for x_bar in range(input_grid.shape[0]):
        if np.all(input_grid[x_bar, :] == Color.GREY):
            break

    for y_bar in range(input_grid.shape[1]):
        if np.all(input_grid[:, y_bar] == Color.GREY):
            break

    # Identify each quadrant
    top_left = input_grid[:x_bar, :y_bar]
    top_right = input_grid[:x_bar, y_bar+1:]
    bottom_left = input_grid[x_bar+1:, :y_bar]
    bottom_right = input_grid[x_bar+1:, y_bar+1:]

    # Create an empty output grid
    output_grid = np.zeros_like(input_grid)

    # Mark intersections that are blue in at least 3 out of 4 quadrants
    condition = ((top_left == Color.BLUE).astype(int) +
                 (top_right == Color.BLUE).astype(int) +
                 (bottom_left == Color.BLUE).astype(int) +
                 (bottom_right == Color.BLUE).astype(int)) >= 3

    output_grid[:x_bar, :y_bar][condition] = Color.RED
    output_grid[:x_bar, y_bar+1:][condition] = Color.RED
    output_grid[x_bar+1:, :y_bar][condition] = Color.RED
    output_grid[x_bar+1:, y_bar+1:][condition] = Color.RED

    return output_grid


def generate_input() -> np.ndarray:
    # Create a grid with a separator
    width, height = 9, 9
    grid = np.zeros((width, height), dtype=int)

    # Add vertical and horizontal grey bars to form four quadrants
    x_bar, y_bar = 4, 4
    grid[x_bar, :] = Color.GREY
    grid[:, y_bar] = Color.GREY

    # Fill each quadrant with random blue or black values
    for region in [(0, 0, x_bar, y_bar), (0, y_bar+1, x_bar, height), (x_bar+1, 0, width, y_bar), (x_bar+1, y_bar+1, width, height)]:
        region_x_start, region_y_start, region_x_end, region_y_end = region
        for x in range(region_x_start, region_x_end):
            for y in range(region_y_start, region_y_end):
                grid[x, y] = np.random.choice([Color.BLUE, Color.BLACK])

    return grid