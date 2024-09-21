from common import *

import numpy as np
from typing import *

# concepts:
# shape completion

# description:
# In the input you will see an incomplete teal ractangle
# To make the output grid, you should use the red color to complete the rectangle.

def main(input_grid):
    # Find the bounding box of the incomplete rectangle and use it to extra the sprite
    x, y, x_len, y_len = bounding_box(grid=input_grid)
    rectangle = input_grid[x:x + x_len, y:y + y_len]

    # Find the missing parts of the rectangle (which are colored black) and complete it with red color
    rectangle_sprite = np.where(rectangle == Color.BLACK, Color.RED, rectangle)

    # Make the output by copying the sprite to a new canvas
    output_grid = np.copy(input_grid)
    output_grid = blit_sprite(grid=output_grid, sprite=rectangle_sprite, x=x, y=y)

    return output_grid

def generate_input():
    # Generate a grid with a size of n x m
    n, m = np.random.randint(7, 15), np.random.randint(7, 15)
    grid = np.zeros((n, m), dtype=int)

    # Randomly generate a rectangle with a size of x_len x y_len, not too big nor too small
    x_len = np.random.randint(n // 2, n - 2)
    y_len = np.random.randint(m // 2, m - 2)

    # Randomly generate a rectangle with a size of x_len x y_len that is incomplete (density < 1)
    rectangle_sprite = random_sprite(n=x_len, m=y_len, color_palette=[Color.TEAL], density=0.3, connectivity=8)

    # Randomly choose a position to draw the rectangle
    x, y = random_free_location_for_sprite(grid=grid, sprite=rectangle_sprite, border_size=1)
    grid = blit_sprite(grid=grid, sprite=rectangle_sprite, x=x, y=y)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
