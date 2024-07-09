from common import *

import numpy as np
from typing import *

# concepts:
# color guide, filling, objects

# description:
# In the input, you will see a colored object in the middle and a single pixel in the bottom left corner of a different color.
# To make the output, remove the pixel from bottom left corner and color the object in the middle with the color from the pixel you removed.

def main(input_grid):
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # get the color of the pixel in the bottom left corner
    color = output_grid[0, -1]

    # remove the pixel from the bottom left corner
    output_grid[0, -1] = Color.BLACK

    # color the object in the middle with the color of the pixel from the bottom left corner
    output_grid = np.where(output_grid, color, output_grid)
    # could also have used flood_fill:
    # x, y = np.where(output_grid != Color.BLACK)
    # flood_fill(output_grid, x[0], y[0], color)

    return output_grid

def generate_input():
    # make 7x7 black grid with black background
    n = m = 7
    grid = np.zeros((n,m), dtype=int)

    # select a color for the sprite
    sprite_color = np.random.choice(list(Color.NOT_BLACK))

    # select a color for the corner pixel
    corner_color = np.random.choice(list(Color.NOT_BLACK))

    # check that colors are different
    # if they are the same then try again
    if sprite_color == corner_color:
        return generate_input()
    
    # make random sprite and put it in middle of grid
    sprite = random_sprite(n-2, m-2, "not_symmetric", [sprite_color])
    blit_sprite(grid, sprite, x=1, y=1)

    # put a single pixel in the bottom left corner
    grid[0, -1] = corner_color

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)