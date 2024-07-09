from common import *

import numpy as np
from typing import *

# concepts:
# horizontal/vertical bars, counting

# description:
# In the input, you will see horizontal and vertical bars, dividing the input into a grid of rectangular regions, on a non-black background.
# To make the output produce a monochromatic image whose width is the number of background-colored regions going left-to-right, and whose height is the number of regions going top-to-bottom.
# The output should have the same background.


def main(input_grid):
    # Plan:
    # 1. Find the color of the background and the bars
    # 2. Count the number of regions going left-to-right
    # 3. Count the number of regions going top-to-bottom

    # Find bar color and background color
    for x in range(input_grid.shape[0]):
        bar_slice = input_grid[x, :]
        if np.all(bar_slice == bar_slice[0]):
            bar_color = bar_slice[0]
            break

    # background is whatever color isn't the bar color
    background = [ color for color in input_grid.flatten() if color != bar_color ][0]

    # Count the number of regions going left-to-right
    n_horizontal = 1
    for x in range(input_grid.shape[0]):
        if input_grid[x, 0] == bar_color:
            n_horizontal += 1
    
    # Count the number of regions going top-to-bottom
    n_vertical = 1
    for y in range(input_grid.shape[1]):
        if input_grid[0, y] == bar_color:
            n_vertical += 1
    
    # Create output grid
    output_grid = np.full((n_horizontal, n_vertical), background)

    return output_grid


def generate_input():
    # Picking background and line colors
    background_color, bar_color = random.sample(list(Color.NOT_BLACK), k=2)

    # Creating the background grid
    n = random.randint(11, 21)
    grid = np.full((n, n), background_color)

    # Create sprites for the bars. We will place them randomly later.
    vertical_line_sprite = np.full((1, n), bar_color)
    horizontal_line_sprite = np.full((n, 1), bar_color)

    # Picking how many lines to have in each dimension
    line_n, line_m = random.randint(1, n // 3), random.randint(1, n // 3)

    # Create separate grids for horizontal and vertical lines, and then merge them later
    # This is because horizontal/vertical are allowed to intersect, but horizontals can't touch each other (and verticals can't touch each other)
    # So we need to do collision detection / free location separately for each type of line
    vertical_line_grid = grid.copy()
    horizontal_line_grid = grid.copy()

    # Verticals
    for i in range(line_n):
        x, y = random_free_location_for_sprite(
            vertical_line_grid,
            vertical_line_sprite,
            background=background_color,
            padding=1
        )
        blit_sprite(vertical_line_grid, vertical_line_sprite, x, y)

    # Horizontals
    for i in range(line_m):
        x, y = random_free_location_for_sprite(horizontal_line_grid, horizontal_line_sprite, background=background_color, padding=1)
        blit_sprite(horizontal_line_grid, horizontal_line_sprite, x, y)

    # Combine the two line grids
    blit_object(grid, vertical_line_grid, background=background_color)
    blit_object(grid, horizontal_line_grid, background=background_color)

    return grid


# ============= remove below this point for prompting =============
if __name__ == "__main__":
    visualize(generate_input, main)
