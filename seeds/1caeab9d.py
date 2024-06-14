from common import *

import numpy as np
from typing import *

# concepts:
# <list of concepts, separated by commas>

# description:
# In the input you will see a red, blue, and yellow shape. Each are the same shape. They occur left to right in the input grid among a black background, but at slightly different vertical heights. The output is the same as the input, but with the vertical heights of the red and yellow shapes adjusted to match the height of the blue shape.

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
    # create a (5-10)x10 input grid
    w = np.random.randint(5, 10)
    h = 10
    grid = np.full((w, h), Color.BLACK, dtype=int)

    # make a random shape of size (1-3)x(1-3)
    w1 = np.random.randint(1, 3)
    h1 = np.random.randint(1, 3)
    # TODO[Simon] replace with random_sprite function when working?
    shape_mask = np.full((w1, h1), Color.BLUE, dtype=int)
    shape_mask[np.random.rand(w1, h1) < 0.1] = Color.BLACK

    # for each color,
    # put a colored form of the shape in a random spot in a (3-4)xh grid
    subgrids = []
    for color in [Color.BLUE, Color.RED, Color.YELLOW]:
        subgrid = np.full((np.random.randint(3, 4), h), Color.BLACK, dtype=int)
        # make the shape in that color
        shape = np.copy(shape_mask)
        shape[shape == Color.BLUE] = color

        x, y = random_free_location_for_object(subgrid, shape)
        blit(subgrid, shape, x, y)
        subgrids.append(subgrid)

    # now concatenate the subgrids along the x axis to make the input grid
    grid = np.concatenate(subgrids, axis=0)
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
