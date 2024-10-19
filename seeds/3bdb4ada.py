from common import *

import numpy as np
from typing import *

# concepts:
# punching holes, geometric pattern

# description:
# In the input you will see a grid with some rectangles. Each rectangle is three pixels along its short side, and is monochromatic.
# To make the output, you should draw black pixels along the middle of each rectangle with a period of 2 starting one pixel in.
# Effectively punching holes in the middle of each rectangle, skipping alternating pixels.

def main(input_grid):
    # Plan:
    # 1. Extract the rectangles from the input grid
    # 2. Canonicalize the rectangles: ensure that they are horizontal (remember to rotate back otherwise)
    # 3. Draw black pixels inside each rectangle (horizontally, skipping every other pixel)
    # 4. Rotate the rectangle back if it was not originally horizontal

    # 1. Extract the rectangles from the input grid
    rectangle_objects = find_connected_components(input_grid, monochromatic=True)

    output_grid = np.full_like(input_grid, Color.BLACK)
    for rectangle_object in rectangle_objects:
        # 2. Canonicalize the rectangle sprite
        original_x, original_y, width, height = bounding_box(rectangle_object, background=Color.BLACK)
        # crop to convert object to sprite
        rectangle_sprite = crop(rectangle_object, background=Color.BLACK)

        # Flip it to be horizontal if it isn't already
        is_horizontal = width > height
        if not is_horizontal:
            rectangle_sprite = np.rot90(rectangle_sprite)
            width, height = height, width

        # 3. Punch holes through the middle of the rectangle
        # The inner row is y=height//2
        for x in range(1, width, 2):
            rectangle_sprite[x, height//2] = Color.BLACK
        
        # 4. Rotate back if it was originally vertical, and then draw it to the output grid
        if not is_horizontal:
            rectangle_sprite = np.rot90(rectangle_sprite, k=-1)
        
        # draw it back in its original location
        blit_sprite(output_grid, rectangle_sprite, original_x, original_y)

    return output_grid

def generate_input():
    # Generate the background grid
    width, height = np.random.randint(10, 30), np.random.randint(10, 20)
    grid = np.zeros((width, height), dtype=int)

    # Randomly choose the number of rectangles on the grid
    num_rectangles = np.random.randint(1, 4)
    # Randomly choose colors for the rectangles
    colors = np.random.choice(Color.NOT_BLACK, num_rectangles, replace=False)

    for color in colors:
        # Randomly choose the width of the rectangle, should not be too short and should be odd
        w, h = np.random.randint(2, 6) * 2 + 1, 3
        rectangle_sprite = np.full((w, h), color)

        # randomly flipped to create different orientations
        if np.random.rand() < 0.5:
            rectangle_sprite = np.rot90(rectangle_sprite)

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
