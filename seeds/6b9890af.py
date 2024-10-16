from common import *

import numpy as np
from typing import *

# concepts:
# object detection, scaling

# description:
# In the input you will see a 3x3 object and a red square n times larger than the 3x3 object.
# To make the output, you should scale the 3x3 object to the size of the red square and place it in the red square.
# Return just the red square (with the rescaled object put into it)

def main(input_grid):
    # Detect the red frame sqaure and the 3x3 pattern square
    objects = detect_objects(input_grid, monochromatic=True, connectivity=8)
    
    # Extract the object, seperate them into the red frame square and the 3x3 pattern square
    for obj in objects:
        sprite = crop(obj, background=Color.BLACK)
        if Color.RED in object_colors(sprite, background=Color.BLACK):
            outer_sprite = sprite
        else:
            inner_sprite = sprite
    
    # Calculate the scaling factor.
    # You need to subtract 2 because the red frame square has 1 pixel border on each side, and there are 2 sides
    scale = (len(outer_sprite) - 2) // len(inner_sprite)

    # Scale the small thing
    scaled_inner_sprite = scale_sprite(inner_sprite, factor=scale)

    # Put them all down on a new output grid
    output_grid = np.full(outer_sprite.shape, Color.BLACK)
    blit_sprite(output_grid, outer_sprite, x=0, y=0, background=Color.BLACK)
    blit_sprite(output_grid, scaled_inner_sprite, x=1, y=1, background=Color.BLACK)

    return output_grid

def generate_input():
    # Initialize the grid
    n, m = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.zeros((n, m), dtype=int)    

    # Set the pattern size and scaling range
    small_object_size = 3
    availabe_scales = range(1, 5)
    scale = np.random.choice(availabe_scales)

    # Generate the red square frame scale times larger than the pattern square and randomly place it
    big_red_rectangle = np.full((scale * small_object_size + 2, scale * small_object_size + 2), Color.RED)
    big_red_rectangle[1:-1, 1:-1] = Color.BLACK
    x_square, y_square = random_free_location_for_sprite(grid, big_red_rectangle)
    grid = blit_sprite(x=x_square, y=y_square, grid=grid, sprite=big_red_rectangle, background=Color.BLACK)

    # Generate the random pattern square with pattern_size
    availabe_color = [c for c in Color.NOT_BLACK if c != Color.RED]
    random_color = np.random.choice(availabe_color)

    # Randomly place the pattern square in the area without the red square
    sprite = random_sprite(n=small_object_size, m=small_object_size, color_palette=[random_color], density=0.5)
    x, y = random_free_location_for_sprite(grid, sprite)
    grid = blit_sprite(x, y, grid, sprite, background=Color.BLACK)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
