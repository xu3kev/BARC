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

    for x, y in np.argwhere(input_grid == Color.BLACK):
        # Check if the current position is between the two objects
        # Also ensure it is not between the borders of the objects (padding=1)
        if check_between_objects(obj1=objects[0], obj2=objects[1], x=x, y=y, padding=1):
            output_grid[x, y] = Color.TEAL
    
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
