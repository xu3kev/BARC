from common import *

import numpy as np
from typing import *

# concepts:
# pixel patterns, counting, expanding, diagonal lines

# description:
# In the input you will see a line with several colored pixels.
# To make the output, create a square grid and place the input line at the bottom-left. Each colored pixel shoots a diagonal line outward toward the upper right.
# The length of the output grid is the product of the number of colored input pixels and the length of the input line.

def main(input_grid):
    # Plan:
    # 1. Figure out how big the output should be and make a blank output grid
    # 2. Place the input line at the bottom left of the output grid
    # 3. Repeatedly translate it diagonally toward the upper right corner, equivalently shooting diagonal lines from each colored pixel

    # 1. The output grid size is the number of non-black pixels in the input grid times the original grid width
    input_width, input_height = input_grid.shape
    num_different_colors = sum(color in input_grid.flatten() for color in Color.NOT_BLACK )
    output_size = input_width * num_different_colors
    output_grid = np.full((output_size, output_size), Color.BLACK)

    # 2-3. Place the input at the bottom left and then move it upward and rightward
    bottommost_y = output_size - 1
    for iteration in range(output_size):
        blit_sprite(output_grid, input_grid, x=iteration, y=bottommost_y - iteration*input_height)

    return output_grid

def generate_input():
    # Generate a line
    width = np.random.randint(3, 7)
    height = 1
    grid = np.full((width, height), Color.BLACK)

    # Randomly choose colors for each grid
    colors = np.random.choice(Color.NOT_BLACK, size=width, replace=False)
    for x in range(width):
        # Randomly assign a color to each pixel
        if np.random.rand() < 0.6:
            grid[x, 0] = colors[x]

    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
