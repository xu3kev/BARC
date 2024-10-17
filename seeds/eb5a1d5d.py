from common import *

import numpy as np
from typing import *

# concepts:
# downscaling

# description:
# In the input you will see a grid consisting of nested shapes of different colors.
# To make the output, make a grid with one pixel for each layer of the shapes, 
# with the color from outermost layer to the innermost layer in the order they appear in the input.

def main(input_grid):
    # Find the objects in the input grid
    objects = find_connected_components(input_grid, connectivity=4, monochromatic=True, background=Color.BLACK)

    # Sort the objects from outermost to innermost
    objects.sort(key=lambda obj: crop(obj).shape[0] * crop(obj).shape[1], reverse=True)

    # Leave only one layer of each color shape
    grid_len = len(objects) * 2 - 1
    output_grid = np.full((grid_len, grid_len), Color.BLACK)

    # Calculate each layer's length and color
    current_len = grid_len
    cur_color = Color.BLACK

    # Draw a nested shape with the colors, each layer has only one pixel length of the current color
    for i, object in enumerate(objects):
        # Get the color of the current layer
        color = object_colors(object)[0]
        # Fill the region with the current color
        cur_shape = np.full((current_len, current_len), color)
        # Place the current shape in the output grid
        # Make sure each layer has only one pixel length of the current color
        blit_sprite(grid=output_grid, sprite=cur_shape, x=i, y=i, background=cur_color)
        cur_color = color
        current_len -= 2

    return output_grid

def generate_input():
    # Get the number of colors
    n_colors = random.randint(2, 6)
    colors = np.random.choice(Color.NOT_BLACK, n_colors, replace=False)

    # Get the innermost shape dimensions
    cur_width, cur_height = np.random.randint(3, 6), np.random.randint(3, 6)
    
    # Draw a nested shape with the colors
    previous_shape = None
    for color in colors:
        # Fill the current shape with the current color
        cur_shape = np.full((cur_width, cur_height), color)
        if previous_shape is not None:
            # Place the previous shape in a random location in the current shape
            x, y = random_free_location_for_sprite(grid=cur_shape, sprite=previous_shape, background=color, border_size=1)
            blit_sprite(grid=cur_shape, sprite=previous_shape, x=x, y=y, background=color)

        # Update the previous shape
        previous_shape = cur_shape
        
        # Update the dimensions of the next shape, should be larger than the previous shape
        next_layer_width, next_layer_height = np.random.randint(cur_width + 2, cur_width + 6), np.random.randint(cur_height + 2, cur_height + 6)
        cur_width, cur_height = next_layer_width, next_layer_height
    
    # The final shape is the last shape with all inner shapes inside each other
    grid = cur_shape
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
