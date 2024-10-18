from common import *

import numpy as np
from typing import *

# concepts:
# geometric pattern

# description:
# In the input you will see a grid with a single coloured pixel.
# To make the output, move the colored pixel down one pixel and draw a yellow line from the pixel to the top of the grid.
# Finally repeat the yellow line by repeating it horizontally left/right with a period of 2 pixels.

def main(input_grid):
    # Plan:
    # 1. Extract the pixel from the input grid
    # 2. Move the pixel one pixel down
    # 3. Draw a yellow line from the pixel to the top of the grid, repeating it horizontally left/right with a period of 2 pixels

    # 1. Extract the pixel
    pixel = find_connected_components(input_grid, monochromatic=True)[0]
    pixel_x, pixel_y = object_position(pixel)
    pixel_color = object_colors(pixel)[0]

    # 2. Move the pixel one pixel down
    output_grid = input_grid.copy()
    output_grid[pixel_x, pixel_y + 1] = pixel_color
    output_grid[pixel_x, pixel_y] = Color.BLACK

    # 3. Draw the vertical line from the pixel to top

    # Draw the line from left to right
    horizontal_period = 2
    for x in range(pixel_x, output_grid.shape[0], horizontal_period):
        draw_line(output_grid, x=x, y=pixel_y, direction=(0, -1), color=Color.YELLOW)

    # Draw the line from left to right
    for x in range(pixel_x, -1, -horizontal_period):
        draw_line(output_grid, x=x, y=pixel_y, direction=(0, -1), color=Color.YELLOW)
    return output_grid

def generate_input():
    # Generate the background grid
    width, height = np.random.randint(5, 30, size=2)
    grid = np.zeros((width, height), dtype=int)

    # Randomly choose one color
    color = np.random.choice([color for color in Color.NOT_BLACK if color != Color.YELLOW])

    # Randomly place the pixel on the grid
    x, y = np.random.randint(0, width - 1), np.random.randint(0, height - 1)
    grid[x, y] = color

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
