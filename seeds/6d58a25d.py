from common import *

import numpy as np
from typing import *

# concepts:
# sliding objects

# description:
# In the input grid, you will see a chevron-shaped object of one color in a black grid, with pixels of another color scattered around the grid.
# To produce the output grid, take all pixels located underneath the chevron. For each of these pixels, extend a vertical line of the same color up and down, until reaching the bottom of the grid or the boundary of the chevron.

def main(input_grid):
    # 1. find the chevron: it is the largest object by size.
    # 2. get the color of the chevron
    # 3. get the color of the colored pixels in the grid.
    # 4. for each colored pixel, check if the chevron is above it. if so, extend a line of the same color above and below it until we reach the bottom of the grid or the boundary of the chevron.

    # get the chevron
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True)
    chevron = max(objects, key=lambda o: np.count_nonzero(o))

    # get the color of the chevron
    chevron_color = chevron[chevron != Color.BLACK][0]

    # get the color of the colored pixels (the other color in the grid)
    colors = np.unique(input_grid)
    colors = [c for c in colors if c not in [Color.BLACK, chevron_color]]
    assert len(colors) == 1
    pixel_color = colors[0]

    # for each colored pixel, check if chevron is above it
    # to do so, iterate through the grid and check for pixel_color.
    # then try moving up until we hit the chevron color.
    # if we do, then paint a vertical line onto the output grid.
    output_grid = input_grid.copy()
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if input_grid[x, y] != pixel_color:
                continue
            # try moving up until we hit the chevron color
            dy = 0
            while y + dy >= 0 and input_grid[x, y + dy] != chevron_color:
                dy = dy - 1

            if input_grid[x, y + dy] == chevron_color:
                # make a line from here to the bottom
                output_grid[x, y + dy + 1:] = pixel_color

    return output_grid


def generate_input():
    # create a 20x20 black grid
    input_grid = np.full((20, 20), Color.BLACK)

    # choose a chevron color and pixel color
    chevron_color, pixel_color = np.random.choice(Color.NOT_BLACK, 2, replace=False)

    # create the chevron
    chevron = np.full((7, 4), Color.BLACK)
    # Create coordinate arrays
    x, y = np.indices(chevron.shape)
    # fill in the chevron
    chevron[np.logical_and(y == 0, x == 3)] = chevron_color
    chevron[np.logical_and(y == 1, np.logical_and(x >= 2, x <= 4))] = chevron_color
    chevron[np.logical_and(y == 2, np.logical_and(x >= 1, x <= 5))] = chevron_color
    chevron[np.logical_and(y == 3, np.logical_or(x == 0, x == 6))] = chevron_color
    # put the chevron at a random location in the upper half of the grid
    x, y = np.random.randint(0, 20 - 7), np.random.randint(0, 10 - 4)
    blit_sprite(input_grid, chevron, x=x, y=y)

    # generate 5-25 pixels at random (unfilled) spots.
    n_pixels = np.random.randint(5, 26)
    x_choices, y_choices = np.where(input_grid == Color.BLACK)
    location_choices = list(zip(x_choices, y_choices))
    pixel_locations = random.sample(location_choices, n_pixels)
    for x, y in pixel_locations:
        input_grid[x, y] = pixel_color

    return input_grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
