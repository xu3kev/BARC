from common import *

import numpy as np
from typing import *

# concepts:
# non-black background, diagonal lines

# description:
# In the input you will see a grid there's all the same color except for a single black pixel in the middle. Equivalently, a black pixel on a non-black background.
# To make the output, draw black diagonal lines outward from the single black pixel in all 4 diagonal directions.

def main(input_grid):
    # Plan:
    # 1. Find the black pixel
    # 2. Draw diagonal lines outward from the black pixel

    # Find the possible locations that are black, then check that there is exactly one
    black_pixel_locations = np.argwhere(input_grid == Color.BLACK)
    assert len(black_pixel_locations) == 1
    black_pixel_location = black_pixel_locations[0]
    black_x, black_y = black_pixel_location

    # We are going to draw on top of the input grid
    output_grid = input_grid.copy()

    # Draw the diagonal lines
    for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        direction = (dx, dy)
        draw_line(output_grid, black_x, black_y, direction=direction, color=Color.BLACK)

    return output_grid

def generate_input():
    # Make a grid with a random background color (not black)
    background_color = np.random.choice(Color.NOT_BLACK)
    width, height = np.random.randint(3, 30, size=2)
    input_grid = np.full((width, height), background_color)

    # Place a black pixel in the middle
    input_grid[width // 2, height // 2] = Color.BLACK

    return input_grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
