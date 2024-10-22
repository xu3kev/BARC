from common import *

import numpy as np
from typing import *

# concepts:
# Expanding, Framing, Growing

# description:
# In the input you will see some squares of different sizes and colors.
# To make the output, you need to:
# 1. Expand the squares down to the bottom of the grid using the color BLUE.
# 2. Draw a green frame around the squares. The green square should be twice as long as the original square.
# 3. Put the original square back to the center of the green square.

def main(input_grid):
    # Plan:
    # 1. Extract the square objects from the input grid
    # 2. Expand the squares down to the bottom using the color BLUE
    # 3. Draw the frame
    # 4. Put the original squares back

    # 1. Input parsing and setup
    # Extract the squares in the input grid
    square_objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)

    # Note the frame color and the expansion down color
    frame_color = Color.GREEN
    expand_color = Color.BLUE

    # The output grid is the same size as the input grid
    output_grid = np.full_like(input_grid, Color.BLACK)

    # 2. Expand the square down to the bottom use color expand_color
    for square_obj in square_objects:
        x, y, w, h = bounding_box(square_obj)
        # Equivalently:
        # output_grid[x:x+w, y+h:] = expand_color
        for i in range(x, x + w):
            draw_line(grid=output_grid, x=i, y=y + h, color=expand_color, direction=(0, 1))
    
    # 3. Draw a green square frame around the original squares, the green square should be twice as big as original were
    for square_obj in square_objects:
        # The square can be partly outside the canvas
        # This math is to get the (x,y) of the top-left corner of the square, even if it's outside the canvas
        x, y, w, h = bounding_box(square_obj)
        square_len = max(w, h)
        x -= (square_len - w)
        y -= (square_len - h)
        # Make and draw the frame
        frame_len = square_len * 2
        green_frame = np.full((frame_len, frame_len), frame_color)
        blit_sprite(output_grid, green_frame, x - square_len // 2, y - square_len // 2)
    
    # 4. Put the original square back to the center of the green square
    for square_obj in square_objects:
        x, y, w, h = bounding_box(square_obj)
        square_obj = crop(square_obj)
        blit_sprite(output_grid, square_obj, x, y)

    return output_grid

def generate_input():
    # Generate the background grid
    width = np.random.randint(15, 30)
    height = width
    grid = np.full((width, height), Color.BLACK)

    # Randomly select the number of squares
    square_num = np.random.randint(2, 5)
    square_color = Color.MAROON

    for _ in range(square_num):
        # Randomly select the size of the squares
        square_size = np.random.randint(1, 4)
        # Ensure the size of square is even
        square_size = square_size * 2

        square = np.full((square_size, square_size), square_color)
        try:
            # Place the square on the grid
            x, y = random_free_location_for_sprite(grid=grid, sprite=square, background=Color.BLACK, padding=2, padding_connectivity=8, border_size=1)
        except:
            # If there is no space, regenerate the input
            return generate_input()
        blit_sprite(grid, square, x, y, Color.BLACK)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
