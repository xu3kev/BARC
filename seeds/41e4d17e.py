from common import *

import numpy as np
from typing import *

# concepts:
# non-black background, occlusion

# description:
# In the input you will see a non-black background (teal background) and the outlines of 5x5 blue rectangles
# To make the output, draw pink horizontal/vertical bars at the center of each rectangle. The bars should be underneath the rectangles, and they should reach the edges of the canvas.

def main(input_grid):
    # Plan:
    # 1. Find the background color; check that it is teal
    # 2. Find the rectangles
    # 3. Draw the pink bars
    # 4. Ensure the rectangles are on top of the bars by drawing the rectangles last

    # The background is the most common color
    background = np.bincount(input_grid.flatten()).argmax()
    assert background == Color.TEAL

    # Extract the objects, which are the outlines of rectangles
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=False, background=background)

    # Each object gets pink bars at its center, but these are going to be drawn over the object, which we have to undo later by redrawing the objects
    for obj in objects:
        center_x, center_y = object_position(obj, anchor='center', background=background)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            draw_line(input_grid, center_x, center_y, direction=(dx, dy), color=Color.PINK)
    
    # Redraw the objects
    for obj in objects:
        blit_object(input_grid, obj, background=background)
    
    return input_grid

def generate_input():
    background_color, rectangle_color = Color.TEAL, Color.BLUE
    width, height = np.random.randint(7, 20, size=2)
    input_grid = np.full((width, height), fill_value=background_color)

    n_rectangles = np.random.randint(1, 3)
    for _ in range(n_rectangles):
        # Create a rectangle and then hollow it out by filling its inside with the background color
        rectangle_sprite = np.full((5, 5), rectangle_color)
        rectangle_sprite[1:-1, 1:-1] = background_color
        # Place the rectangle randomly, taking care though that it does not touch or overlap any other rectangles
        x, y = random_free_location_for_sprite(input_grid, rectangle_sprite, background=background_color, padding=1, border_size=1)
        blit_sprite(input_grid, rectangle_sprite, x, y, background=background_color)

    return input_grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
