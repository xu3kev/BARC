from common import *

import numpy as np
from typing import *

# concepts:
# object detection, pattern drawing

# description:
# In the input you will see two blue pixels
# To make the output grid, you should place a 3x3 green cross pattern between the two blue pixels exactly halfway between them.

def main(input_grid):
    # Detect the two blue pixels on the grid.
    blue_pixels = detect_objects(grid=input_grid, colors=[Color.BLUE], monochromatic=True, connectivity=4)

    # Get the position of the two blue pixels.
    x_two, y_two = [], []
    for blue_pixel in blue_pixels:
        x, y, _, _ = bounding_box(grid=blue_pixel)
        x_two.append(x)
        y_two.append(y)
    
    # Find out if the two blue pixels are horizontal or vertical.
    if_horizontal = y_two[0] == y_two[1]

    # Generate the 3x3 green cross pattern between the two blue pixels.
    object_pattern = np.array( [[Color.BLACK, Color.GREEN, Color.BLACK],
                                [Color.GREEN, Color.GREEN, Color.GREEN],
                                [Color.BLACK, Color.GREEN, Color.BLACK]])
    output_grid = input_grid.copy()

    # Place the 3x3 green cross pattern between the middle of two blue pixels.
    if if_horizontal:
        output_grid = blit_sprite(grid=output_grid, sprite=object_pattern, x=x_two[0] + 2, y=y_two[0] - 1)
    else:
        output_grid = blit_sprite(grid=output_grid, sprite=object_pattern, x=x_two[0] - 1, y=y_two[0] + 2)
    return output_grid

def generate_input():
    # Generate the background grid with size of n x m.
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)

    # Randomly choose if the two blue pixels are horizontal or vertical.
    if_horizontal  = np.random.choice([True, False])

    # Randomly place two blue pixels on the grid with a distance of 5 pixels.
    line_width = 5

    # Ensure there is enough space for the 3 x 3 green cross pattern and two blue pixels.
    if if_horizontal:
        x = np.random.randint(0, n - 6)
        y = np.random.randint(1, m - 1)
        grid[x, y] = Color.BLUE
        grid[x + line_width + 1, y] = Color.BLUE
    else:
        x = np.random.randint(1, n - 1)
        y = np.random.randint(0, m - 6)
        grid[x, y] = Color.BLUE
        grid[x, y + line_width + 1] = Color.BLUE

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
