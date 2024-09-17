from common import *

import numpy as np
from typing import *

# concepts:
# object detection, cropping, scaling, 

# description:
# In the input you will see a 3x3 pattern square and a red square n times larger than the pattern square.
# To make the output, you should scale the pattern square to the size of the red square and place it in the red square.

def main(input_grid):
    # Detect the red frame squre and the 3x3 pattern square
    find_grid = detect_objects(grid=input_grid, monochromatic=True, connectivity=8)
    
    # Extract the object, seperate them into the red frame square and the 3x3 pattern square
    for obj in find_grid:
        cropped_obj = crop(grid=obj, background=Color.BLACK)
        if np.any(cropped_obj == Color.RED):
            bounding_box_obj = cropped_obj
        else:
            inner_obj = cropped_obj
    
    # Calculate the scale of the pattern square
    scale = len(bounding_box_obj - 2) // len(inner_obj)

    # Scale the pattern square scale times larger
    scaled_inner_object = []
    for row in inner_obj:
        new_row = []
        for item in row:
            new_row.extend([item] * scale)
        scaled_inner_object.extend([new_row] * scale)
    scaled_inner_object = np.array(scaled_inner_object)

    # Place the scaled pattern square in the red frame square
    output_grid = blit_sprite(x=1, y=1, grid=bounding_box_obj, sprite=scaled_inner_object, background=Color.BLACK)
    return output_grid

def generate_input():
    # Initialize the grid
    n, m = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.zeros((n, m), dtype=int)    

    # Set the pattern size and scaling range
    pattern_size = 3
    availabe_scale = range(1, 5)
    scale = np.random.choice(availabe_scale)

    # Generate the red square scale times larger than the pattern square and randomly place it
    pattern_square = random_sprite(n=scale * pattern_size + 2, m=scale * pattern_size + 2, color_palette=[Color.RED], density=1.0)
    x_square, y_square = random_free_location_for_sprite(grid, pattern_square)
    grid = blit_sprite(x=x_square, y=y_square, grid=grid, sprite=pattern_square, background=Color.BLACK)

    # Generate the random pattern square with pattern_size
    availabe_color = [c for c in Color.NOT_BLACK if c != Color.RED]
    random_color = np.random.choice(availabe_color)

    # Randomly place the pattern square in the area without the red square
    pattern = random_sprite(n=pattern_size, m=pattern_size, color_palette=[random_color], density=0.5)
    x_pos, y_pos = random_free_location_for_sprite(grid, pattern)
    grid = blit_sprite(x=x_pos, y=y_pos, grid=grid, sprite=pattern, background=Color.BLACK)

    # Only retain the frame of the red square, make it hollow
    pattern_inner = random_sprite(n=scale * pattern_size, m=scale * pattern_size, color_palette=[Color.BLACK], density=1.0, background=Color.RED)
    grid = blit_sprite(x=x_square + 1, y=y_square + 1, grid=grid, sprite=pattern_inner, background=Color.RED)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
