from common import *

import numpy as np
from typing import *

# concepts:
# downscaling

# description:
# In the input you will see a grid consisting of a chessboard pattern of different colors.
# Each chessboard cell is filled with a single color, and has a different size.
# To make the output, make a grid with one pixel for each cell of the chessboard.

def main(input_grid):
    # Find the color objects in the input grid
    objects = find_connected_components(grid=input_grid, connectivity=4, monochromatic=True, background=Color.BLACK)

    # Get the position of the objects
    x_position_list = [object_position(obj)[0] for obj in objects]
    y_position_list = [object_position(obj)[1] for obj in objects]

    # Sort the position list, and get the unique position list since
    # the pattern is separated as chessboard
    x_position_list = sorted(np.unique(x_position_list))
    y_position_list = sorted(np.unique(y_position_list))

    # Get the size of chessboard with one pixel represents the original region
    w_color, h_color = len(x_position_list), len(y_position_list)
    output_grid = np.full((w_color, h_color), Color.BLACK)

    for i, x in enumerate(x_position_list):
        for j, y in enumerate(y_position_list):
            # Use one pixel to represent the original region
            output_grid[i % w_color, j % h_color] = input_grid[x, y]

    return output_grid

def generate_input():
    # Randomly choose the color size
    color_w, color_h = np.random.randint(2, 4), np.random.randint(2, 4)
    colors = np.random.choice(Color.NOT_BLACK, color_w * color_h, replace=True)

    # Randomly choose the pattern size 
    pattern_w, pattern_h = np.random.randint(15, 20), np.random.randint(15, 20)

    # Randomly separate the pattern into colors
    horizontal_separation = generate_position_has_interval(max_len=pattern_w, position_num=color_w, if_padding=True)
    vertical_separation = generate_position_has_interval(max_len=pattern_h, position_num=color_h, if_padding=True)

    # Assign the colors to the pattern by the separation
    pattern = np.zeros((pattern_w, pattern_h), dtype=int)
    for i in range(color_w):
        for j in range(color_h):
            x1 = horizontal_separation[i]
            x2 = horizontal_separation[i + 1] if i + 1 < len(horizontal_separation) else pattern_w
            y1 = vertical_separation[j]
            y2 = vertical_separation[j + 1] if j + 1 < len(vertical_separation) else pattern_h

            pattern[x1:x2, y1:y2] = colors[i * color_h + j]
    
    # Randomly place the pattern in the grid
    # The grid size is larger than the pattern size
    n, m = np.random.randint(pattern_w + 1, 30), np.random.randint(pattern_h + 1, 30)
    grid = np.full((n, m), Color.BLACK)
    x, y = random_free_location_for_sprite(grid=grid, sprite=pattern, background=Color.BLACK)
    blit_sprite(grid=grid, sprite=pattern, x=x, y=y, background=Color.BLACK)

    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
