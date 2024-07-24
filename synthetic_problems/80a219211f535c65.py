from common import *

import numpy as np
from typing import *

# concepts:
# borders, flood fill, connectivity, objects

# description:
# In the input grid, you will see various colored squares surrounded by a black background. 
# There might be some smaller colored pixels scattered around inside these black and white regions.
# To make the output, identify the objects (connected regions) and draw a border with a new color around each object.
# The border should have a thickness of one pixel. The border color should be uniform for all objects.


def main(input_grid):
    # Create a copy of the input grid for the output
    output_grid = np.copy(input_grid)

    # Determine the dimensions of the grid
    n, m = input_grid.shape

    # Define the border color
    border_color = Color.GREY

    # Identify connected components of objects in the grid
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=False)
    
    for obj in objects:
        # Find the bounding box of the object
        x, y, obj_width, obj_height = bounding_box(obj, background=Color.BLACK)
        
        # Define the top-left and bottom-right corners of the bounding box
        top_left_x, top_left_y = x, y
        bottom_right_x, bottom_right_y = x + obj_width - 1, y + obj_height - 1
        
        # Draw the border around the object
        draw_line(output_grid, top_left_x, top_left_y, length=obj_width, color=border_color, direction=(1, 0))
        draw_line(output_grid, top_left_x, top_left_y, length=obj_height, color=border_color, direction=(0, 1))
        draw_line(output_grid, bottom_right_x, bottom_right_y, length=obj_width, color=border_color, direction=(-1, 0))
        draw_line(output_grid, bottom_right_x, bottom_right_y, length=obj_height, color=border_color, direction=(0, -1))
    
    return output_grid

def generate_input():
    # Create a random grid size between 10x10 and 15x15
    width, height = np.random.randint(10, 16), np.random.randint(10, 16)
    grid = np.zeros((width, height), dtype=int)
    
    # Randomly generate 3 to 6 different colored objects
    num_objects = np.random.randint(3, 7)
    for _ in range(num_objects):
        # Randomly size the object
        obj_width, obj_height = np.random.randint(2, 4), np.random.randint(2, 4)
        # Generate a random color for the object
        color = np.random.choice(list(Color.NOT_BLACK))
        # Create the sprite of the object
        sprite = np.full((obj_width, obj_height), color)
        
        # Find a random free location for the sprite in the grid
        x, y = random_free_location_for_sprite(grid, sprite, border_size=1)
        
        # Place the object onto the grid
        blit_sprite(grid, sprite, x, y)
    
    # Randomly add smaller colored dots
    num_dots = np.random.randint(5, 10)
    for _ in range(num_dots):
        color = np.random.choice(list(Color.NOT_BLACK))
        pixel = np.full((1, 1), color)
        x, y = random_free_location_for_sprite(grid, pixel, border_size=1)
        blit_sprite(grid, pixel, x, y)

    return grid