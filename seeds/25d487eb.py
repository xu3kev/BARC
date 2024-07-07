from common import *

import numpy as np
from typing import *


# concepts:
# patterns, growing, horizontal/vertical bars

# description:
# In the input you will see a colored triangle with a single pixel centered in the base of the triangle that is a different color.
# Grow a bar out of and away from the triangle, as if shot out of the tip opposite the differently colored pixel. This bar is the same color as that base pixel.

def main(input_grid):
    # get output grid ready
    output_grid = input_grid

    # find the differently colored pixel
    colors, counts = np.unique(input_grid, return_counts=True)
    base_color = colors[np.argmin(counts)]

    # find the base location and coordinates from it
    base = np.argwhere(input_grid == base_color).flatten()
    [base_x, base_y] = base

    # find which side of the base is not in the triangle
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        # check if this direction would be outside the grid
        x0, y0 = base_x + dx, base_y + dy
        if 0 <= x0 < len(input_grid) and 0 <= y0 < len(input_grid[0]):
            # check if this direction is in the triangle or not
            if input_grid[x0, y0] != Color.BLACK:
                continue
        # this direction is the opposite of the tip, so grow the bar in the opposite direction from the first black pixel
        x0, y0 = base_x - dx, base_y - dy
        while 0 <= x0 < len(input_grid) and 0 <= y0 < len(input_grid[0]):
            if input_grid[x0, y0] == Color.BLACK:
                output_grid[x0, y0] = base_color
            x0, y0 = x0 - dx, y0 - dy

        return output_grid

    assert 0, "No valid slide found"


def generate_input():
    # first choose a random size for the triangle
    size = random.randint(2, 4)
    width = size*2 + 1
    height = size + 1

    # choose a random color for the triangle
    triangle_color = np.random.choice(Color.NOT_BLACK)

    # choose a random color for the base pixel that is not the same as the triangle color
    base_color = np.random.choice(Color.NOT_BLACK)
    while base_color == triangle_color:
        base_color = np.random.choice(Color.NOT_BLACK)

    # create just the triangle on a black grid for the background
    triangle_sprite = np.zeros((width, height), dtype=int)

    # fill in the triangle
    for i in range(height):
        for j in range(i, width - i):
            triangle_sprite[i, j] = triangle_color

    # recolor the base pixel
    triangle_sprite[size, 0] = base_color

    # now make a larger black grid for the background
    n, m = random.randint(10, 16), random.randint(10, 16)
    grid = np.zeros((n, m), dtype=int)

    # randomly choose the triangle's orientation by rotating 0 to 3 times
    rotations = random.randint(0, 3)
    triangle_sprite = np.rot90(triangle_sprite, rotations)

    # choose a random location on the grid, ensuring at least 2 empty pixlels on each edge
    x = random.randint(2, n - width - 2)
    y = random.randint(2, m - height - 2)

    # place the triangle onto the grid
    blit_sprite(grid, triangle_sprite, x, y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)