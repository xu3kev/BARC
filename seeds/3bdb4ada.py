from common import *

import numpy as np
from typing import *

# concepts:
# punching holes, geometric pattern

# description:
# In the input you will see a grid with some rectangles. Each rectangle is three pixels tall and is monochromatic.
# To make the output, you should draw black pixels through the middle have each rectangle with a horizontal period of 2 starting one pixel in from the left.
# Effectively punching holes in the middle of each rectangle, skipping alternating pixels.

def main(input_grid):
    # Plan:
    # 1. Extract the rectangles from the input grid
    # 2. Draw black pixels inside each rectangle

    # 1. Extract the rectangles from the input grid
    rectangle_objects = find_connected_components(input_grid, monochromatic=True)

    # 2. Draw patterns in rectangles: turn inner pixels to black, alternatingly
    output_grid = np.full_like(input_grid, Color.BLACK)
    for rectangle_object in rectangle_objects:
        rectangle_sprite = crop(rectangle_object, background=Color.BLACK)
        w, h = rectangle_sprite.shape
        
        # The inner part is h//2
        for x in range(1, w, 2):
            rectangle_sprite[x, h//2] = Color.BLACK
        
        x, y = object_position(rectangle_object)
        output_grid = blit_sprite(output_grid, rectangle_object, x, y)

    return output_grid

def generate_input():
    # Generate the background grid
    width, height = np.random.randint(10, 30), np.random.randint(10, 20)
    grid = np.zeros((width, height), dtype=int)

    # Randomly choose the number of rectangles on the grid
    rectangle_number = np.random.randint(1, 4)
    # Randomly choose colors for the rectangles
    colors = np.random.choice(Color.NOT_BLACK, rectangle_number, replace=False)

    for color in colors:
        # Randomly choose the width of the rectangle, should not be too short and should be odd
        w, h = np.random.randint(2, 6) * 2 + 1, 3
        rectangle_sprite = np.full((w, h), color)

        # Randomly choose the position of the rectangle
        try:
            x, y = random_free_location_for_sprite(grid, rectangle_sprite, padding=1, padding_connectivity=8)
        except:
            # If there is no free location for the rectangle, retry
            return generate_input()
        blit_sprite(grid, rectangle_sprite, x, y)

    return grid
# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
