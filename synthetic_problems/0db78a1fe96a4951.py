from common import *

import numpy as np
from typing import *

# concepts:
# color mapping, diagonal lines, objects

# description:
# The input contains a black grid with several objects of the same random color. 
# Each object is a 3x3 grid with a different configuration of the same color.
# To make the output, replace each 3x3 object with a diagonal line that starts
# from the center of the object's bounding box and spans the entire grid. The diagonal
# lines will follow the same color mapping: green -> yellow, blue -> gray, red -> pink, teal -> maroon,
# yellow -> green, gray -> blue, pink -> red, maroon -> teal.

def main(input_grid):
    # color mapping
    color_map = {Color.GREEN : Color.YELLOW, 
                 Color.BLUE : Color.GREY, 
                 Color.RED : Color.PINK,
                 Color.TEAL : Color.MAROON,
                 Color.YELLOW : Color.GREEN, 
                 Color.GREY : Color.BLUE, 
                 Color.PINK : Color.RED,
                 Color.MAROON : Color.TEAL}
    
    output_grid = np.copy(input_grid)

    # Detect 3x3 objects
    objects = detect_objects(input_grid, background=Color.BLACK, allowed_dimensions=[(3, 3)], monochromatic=True)
    
    for obj in objects:
        x, y, width, height = bounding_box(obj)
        obj_color = input_grid[x, y]

        # Perform color mapping
        new_color = color_map.get(obj_color, obj_color)

        # Replace the 3x3 object with diagonal lines centered at (x + 1, y + 1)
        center_x, center_y = x + width // 2, y + height // 2
        draw_line(output_grid, center_x, center_y, length=None, color=new_color, direction=(1, 1))
        draw_line(output_grid, center_x, center_y, length=None, color=new_color, direction=(1, -1))
        draw_line(output_grid, center_x, center_y, length=None, color=new_color, direction=(-1, 1))
        draw_line(output_grid, center_x, center_y, length=None, color=new_color, direction=(-1, -1))

    return output_grid


def generate_input():
    n = m = np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)
    
    # Select a random color for the objects
    obj_color = random.choice(list(Color.NOT_BLACK))

    # Generate 3x3 objects
    for _ in range(np.random.randint(3, 7)):
        obj = random_sprite(3, 3, density=0.5, color_palette=[obj_color], symmetry='not_symmetric')
        x, y = random_free_location_for_sprite(grid, obj, padding=3)
        blit_sprite(grid, obj, x, y)
    
    return grid