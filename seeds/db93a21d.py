from common import *

import numpy as np
from typing import *

# concepts:
# Expanding, Framing

# description:
# In the input you will see some squares of different sizes and colors.
# To make the output, you need to:
# 1. Expand the squares down to the bottom of the grid using the color BLUE.
# 2. Draw a green frame around the squares. The green square should be one time larger than the original square.
# 3. Put the original square back to the center of the green square.

def main(input_grid):
    # Extract the squares from the input grid
    squares = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)

    # Observe the frame color and the expand color
    frame_color = Color.GREEN
    expand_color = Color.BLUE

    # The output grid is the same size as the input grid
    output_grid = np.zeros_like(input_grid)

    # STEP 1: Expand the square down to the bottom use color expand_color
    for square in squares:
        x, y, w, h = bounding_box(square)
        for i in range(x, x + w):
            draw_line(grid=output_grid, x=i, y=y + h, color=expand_color, direction=(0, 1))
    
    # STEP 2: Draw a green square frame around the squares, the green square should be one time larger than the original square
    for square in squares:
        x, y, w, h = bounding_box(square)
        # Square can be partially out of the grid
        square_len = max(w, h)
        x = x - (square_len - w)
        y = y - (square_len - h)

        green_square = np.full((square_len * 2, square_len * 2), frame_color)
        blit_sprite(grid=output_grid, sprite=green_square, x=x - square_len // 2, y=y - square_len // 2)
    
    # STEP 3: Put the original square back to the center of the green square
    for square in squares:
        x, y, w, h = bounding_box(square)
        square = crop(square)
        blit_sprite(grid=output_grid, sprite=square, x=x, y=y, background=frame_color)

    return output_grid

def generate_input():
    # Generate the background grid
    n = np.random.randint(15, 30)
    m = n
    grid = np.full((n, m), Color.BLACK)

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
