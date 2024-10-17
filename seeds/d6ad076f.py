from common import *

import numpy as np
from typing import *

# concepts:
# connected components

# description:
# In the input you will see two rectangles separated by a gap.
# To make the output, you need to connect the two rectangles with a teal line.

def main(input_grid):
    # Copy the input grid as output
    output_grid = input_grid.copy()

    # Detect the objects
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)

    # First find out if they can be connected horizontally
    objects = sorted(objects, key=lambda x: object_position(x)[0])

    # There are two objects in the input
    x1, y1, w1, h1 = bounding_box(objects[0])
    x2, y2, w2, h2 = bounding_box(objects[1])

    connect = False

    # Connect component color
    connect_color = Color.TEAL

    # If the left one is higher than the right one and they can be connected horizontally
    if y1 <= y2 and y1 + h1 >= y2:
        # We can connect them horizontally
        for y in range(y2 + 1, min(y1 + h1, y2 + h2) - 1):
            draw_line(grid=output_grid, x=x1 + w1, y=y, end_x=x2 - 1, end_y=y, direction=(1, 0), color=connect_color)
            connect = True
    # If the right one is higher than the left one and they can be connected horizontally
    elif y2 <= y1 and y2 + h2 >= y1:
        # We can connect them horizontally
        for y in range(y1, min(y1 + h1, y2 + h2) - 1):
            draw_line(grid=output_grid, x=x1 + w1, y=y, end_x=x2 - 1, end_y=y, direction=(1, 0), color=connect_color)
            connect = True
    
   
    # If we can't connect them horizontally, try vertically
    objects = sorted(objects, key=lambda x: object_position(x)[1])

    # There are two objects in the input
    x1, y1, w1, h1 = bounding_box(objects[0])
    x2, y2, w2, h2 = bounding_box(objects[1])

    # If the top one is to the left of the bottom one and they can be connected vertically
    if x1 <= x2 and x1 + w1 >= x2:
        # We can connect them vertically
        for x in range(x2 + 1, min(x1 + w1, x2 + w2) - 1):
            draw_line(grid=output_grid, x=x, y=y1 + h1, end_x=x, end_y=y2 - 1, direction=(0, 1), color=connect_color)
            connect = True
    # If the top one is to the right of the bottom one and they can be connected vertically
    elif x2 <= x1 and x2 + w2 >= x1:
        # We can connect them vertically
        for x in range(x1 + 1, min(x1 + w1, x2 + w2) - 1):
            draw_line(grid=output_grid, x=x, y=y1 + h1, end_x=x, end_y=y2 - 1, direction=(0, 1), color=connect_color)
            connect = True
    
    assert connect, "The two objects can't be connected horizontally or vertically."
    return output_grid


def generate_input():
    # Generate the background grid
    n, m = np.random.randint(10, 20, size=2)
    grid = np.full((n, m), Color.BLACK)

    # Choose two colors for the pattern
    color_connect = Color.TEAL
    colors = np.random.choice([color for color in Color.NOT_BLACK if color != color_connect], 2, replace=False)
    color1, color2 = colors

    # Generate two rectangles
    n1, m1 = np.random.randint(3, 10, size=2)
    n2, m2 = np.random.randint(3, 10, size=2)

    rectangle1 = np.full((n1, m1), color1)
    rectangle2 = np.full((n2, m2), color2)

    # Place the rectangles on the grid
    x1, y1 = random_free_location_for_sprite(grid=grid, sprite=rectangle1, background=Color.BLACK, padding=2, padding_connectivity=8)
    blit_sprite(grid, rectangle1, x1, y1, Color.BLACK)
    try:
        # Check if there is enough space for the second rectangle
        x2, y2 = random_free_location_for_sprite(grid=grid, sprite=rectangle2, background=Color.BLACK, padding=2, padding_connectivity=8)
        blit_sprite(grid, rectangle2, x2, y2, Color.BLACK)
        # Ensure the two rectangles can be connected
        main(grid)
    except Exception as e:
        # If not, regenerate the input
        return generate_input()

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
