from common import *

import numpy as np
from typing import *

# concepts:
# alignment, objects

# description:
# In the input you will see a red, blue, and yellow shape. Each are the same shape (but different color). They occur left to right in the input grid on a black background, but at different vertical heights.
# The output is the same as the input, but with the vertical heights of the red and yellow shapes adjusted to match the height of the blue shape.

def main(input_grid):
    # find the blue shape, red shape, and yellow shape
    blue_coords = np.where(input_grid == Color.BLUE)
    red_coords = np.where(input_grid == Color.RED)
    yellow_coords = np.where(input_grid == Color.YELLOW)

    # set the vertical height of the red and yellow shape to match
    red_coords = (red_coords[0], blue_coords[1])
    yellow_coords = (yellow_coords[0], blue_coords[1])

    # make output grid with the colored shapes at their new locations
    output_grid = np.full_like(input_grid, Color.BLACK)
    output_grid[blue_coords] = Color.BLUE
    output_grid[red_coords] = Color.RED
    output_grid[yellow_coords] = Color.YELLOW

    return output_grid


def generate_input():

    # All three shapes are the same shape, but different colors, so we generate one sprite and color it three ways
    # We put each sprite in a different grid, and concatenate the grids to make the input grid

    # make a random sprite of size (1-4)x(1-4)
    w = np.random.randint(1, 5)
    h = np.random.randint(1, 5)
    sprite = random_sprite(w, h)

    # Figure out the height of the output grid
    # This has to be the same across all three colors, because we concatenate them along the x axis
    grid_height = np.random.randint(h+1, 16)

    # for each color,
    # put a colored form of the shape in a random spot in a new grid
    subgrids = []
    for color in [Color.BLUE, Color.RED, Color.YELLOW]:
        # make a grid to put the shape in
        # the grid should be wide enough to fit the shape, which has width w
        grid_width = np.random.randint(w, 30//3)
        subgrid = np.full((grid_width, grid_height), Color.BLACK, dtype=int)

        # make the shape that color
        colored_sprite = np.copy(sprite)
        colored_sprite[sprite != Color.BLACK] = color

        # put the shape in a random spot in its grid
        x, y = random_free_location_for_sprite(subgrid, colored_sprite)
        blit_sprite(subgrid, colored_sprite, x, y)
        subgrids.append(subgrid)

    # now concatenate the subgrids along the x axis to make the input grid
    grid = np.concatenate(subgrids, axis=0)
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
