from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation

# description:
# In the input you will see a grid with a pixel.
# To make the output, you should draw a yellow line from the pixel to the top of the grid, repeat the line every two pixels width,
# and move the pixel one pixel down.

def main(input_grid):
    # Create output grid
    output_grid = input_grid.copy()

    # Extract the pixel
    pixel = find_connected_components(input_grid, monochromatic=True)[0]
    x, y = object_position(pixel)
    pixel_color = object_colors(pixel)[0]

    # Draw the vertical line from the pixel to top, repeat the line every two pixels width
    # Draw the line from right to left
    for i in range(x, -1, -2):
        draw_line(output_grid, x=i, y=y, direction=(0, -1), color=Color.YELLOW)

    # Draw the line from left to right
    for i in range(x, input_grid.shape[0], 2):
        draw_line(output_grid, x=i, y=y, direction=(0, -1), color=Color.YELLOW)
    
    # Move the pixel one pixel down
    output_grid[x, y + 1] = pixel_color

    return output_grid

def generate_input():
    # Generate the background grid
    n, m = np.random.randint(20, 30, size=2)
    grid = np.zeros((n, m), dtype=int)

    # Randomly choose one color
    color = np.random.choice([color for color in Color.NOT_BLACK if color != Color.YELLOW])

    # Randomly place the pixel on the grid
    x, y = np.random.randint(0, n - 1), np.random.randint(0, m - 1)
    grid[x, y] = color

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
