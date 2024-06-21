from common import *

import numpy as np
from typing import *


# concepts:
# filling, counting, horizontal/vertical bars, partitioning

# description:
# In the input you will see a grid with multiple grey bars partitioning the grid into sections, a black background, and a special color. Each section may have 0 or more special color pixels.
# Across all sections in the grid, fill in the section with the special color if the number of special color pixels in that section is equal to the highest number of special color pixels in any section. Otherwise, fill in the section with black.

def main(input_grid):
    # first get the grid size and the special color
    n, m = input_grid.shape
    special_color = (set(np.unique(input_grid)) - {Color.BLACK, Color.GREY}).pop()

    # we want to recolor the grid to use connected components to find the partitions, so we first prepare the output grid and make all special color pixels black
    output_grid = input_grid.copy()
    output_grid[output_grid == special_color] = Color.BLACK

    # before we can find the partitions, we will recolor all the grey bars to black and the black background to grey
    input_grid[input_grid == Color.BLACK] = Color.GREY
    input_grid[output_grid == Color.GREY] = Color.BLACK

    # find the connected components in the grid with black as the background color, giving us the partitions
    partitions = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=False)

    # now we find the maximum number of special color pixels in any section
    max_special_color_pixels = max([np.count_nonzero(partition == special_color) for partition in partitions])

    # for each partition, if the number of special color pixels is equal to the maximum, fill the corresponding output with the special color, otherwise fill it with black
    for partition in partitions:
        if np.count_nonzero(partition == special_color) == max_special_color_pixels:
            output_grid[partition != Color.BLACK] = special_color
        else:
            output_grid[partition != Color.BLACK] = Color.BLACK
        
    return output_grid


def generate_input():
    # first create a 11x11 grid with a black background and 2 evenly spaced horizontal and vertical grey bars
    n, m = 11, 11
    grid = np.full((n, m), Color.BLACK)
    draw_line(grid, 0, 3, length=None, color=Color.GREY, direction=(1, 0))
    draw_line(grid, 0, 7, length=None, color=Color.GREY, direction=(1, 0))
    draw_line(grid, 3, 0, length=None, color=Color.GREY, direction=(0, 1))
    draw_line(grid, 7, 0, length=None, color=Color.GREY, direction=(0, 1))

    # now we want to randomly change each non-grey pixel to the special color with a 20% chance
    special_color = new_random_color(not_allowed_colors=[Color.GREY])
    for i in range(n):
        for j in range(m):
            if grid[i, j] != Color.GREY and random.random() < 0.2:
                grid[i, j] = special_color

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)