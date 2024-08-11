from common import *

import numpy as np
from typing import *

# concepts:
# occlusion, reflection

# description:
# In the input you will see three regions separated by red horizontal bars. Each region is rectangular and the regions are arranged vertically, so there is a top region, middle region, and a bottom region.
# The regions display a yellow pattern, a maroon pattern, and a blue pattern from top to bottom.
# To make the output, you have to copy the blue pattern first, then overlay the left-right reflected maroon pattern over that, and finally overlay the yellow pattern over that as well.

def main(input_grid):
    # find the location of the horizontal red bars that separate the three sections
    red_bars = np.where(input_grid == Color.RED)

    # get the unique y-coordinates of the red bars
    red_bars_y = np.unique(red_bars[1])

    # get the blue pattern from the bottom section and copy it to make the base of the output grid
    blue_pattern = input_grid[:, red_bars_y[1]+1:]
    output_grid = blue_pattern
    # could also have used blit_sprite here
    # output_grid = blit_sprite(output_grid, blue_pattern, x=0, y=0)

    # get the maroon pattern from the middle section, reflect it horizontally, and overlay it on output grid
    maroon_pattern = input_grid[:, red_bars_y[0]+1:red_bars_y[1]]
    reflected_maroon_pattern = maroon_pattern[:, ::-1]
    output_grid = np.where(reflected_maroon_pattern, reflected_maroon_pattern, output_grid)
    # could also have used blit here
    # output_grid = blit_sprite(output_grid, reflected_maroon_pattern, x=0, y=0)

    # get the yellow pattern from the top section and overlay it on output grid
    yellow_pattern = input_grid[:, 0:red_bars_y[0]]
    output_grid = np.where(yellow_pattern, yellow_pattern, output_grid)
    # could also have used blit here
    # output_grid = blit_sprite(output_grid, yellow_pattern, x=0, y=0)

    return output_grid

def generate_input():
    # make a red divider to be used to separate the three sections
    red_divider = np.full((4, 1), Color.RED, dtype=int)

    # make a yellow section and scatter yellow pixels in it
    yellow_section = np.zeros((4, 4), dtype=int)
    for _ in range(12):
        x, y = np.random.randint(yellow_section.shape[1]), np.random.randint(yellow_section.shape[0])
        yellow_section[y, x] = Color.YELLOW

    # make a maroon section and scatter maroon pixels in it
    maroon_section = np.zeros((4, 4), dtype=int)
    for _ in range(12):
        x, y = np.random.randint(maroon_section.shape[1]), np.random.randint(maroon_section.shape[0])
        maroon_section[y, x] = Color.MAROON

    # make a blue section and scatter blue pixels in it
    blue_section = np.zeros((4, 4), dtype=int)
    for _ in range(12):
        x, y = np.random.randint(blue_section.shape[1]), np.random.randint(blue_section.shape[0])
        blue_section[y, x] = Color.BLUE

    # concatenate the three sections with the red dividers
    grid = np.concatenate([yellow_section, red_divider, maroon_section, red_divider, blue_section], axis=1)

    return grid