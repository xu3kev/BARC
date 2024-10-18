from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation

# description:
# In the input you will see a grid with two colored pixels.
# To make the output, you should draw a pattern from the two pixels.
# step 1: draw a horizontal line outward from the two pixels in their respective colours.
# step 2: draw a border around the canvas whose top half is colored to match the top pixel and whose bottom half matches the bottom pixel.


def main(input_grid):
    # Plan:
    # 1. Parse the input and determine which pixel is top in which is bottom
    # 2. Draw horizontal lines
    # 3. Draw border, colored appropriately

    # 1. Input parsing
    # Detect the two pixels, sorting by Y coordinate so top one is first, bottom one is second
    background = Color.BLACK
    pixels = find_connected_components(input_grid, monochromatic=True, background=background)
    pixels.sort(key=lambda obj: object_position(obj, background=background)[1])

    # 2. Draw a horizontal lines outward pixels
    output_grid = np.full_like(input_grid, background)
    for pixel in pixels:
        x, y = object_position(pixel, background=background)
        color = object_colors(pixel, background=background)[0]
        draw_line(output_grid, x=0, y=y, direction=(1, 0), color=color)
    
    # 3. Make a border colored appropriately
    top_color = object_colors(pixels[0], background=background)[0]
    bottom_color = object_colors(pixels[1], background=background)[0]
    draw_line(output_grid, x=0, y=0, direction=(1, 0), color=top_color)
    draw_line(output_grid, x=0, y=0, direction=(0, 1), color=top_color)
    draw_line(output_grid, x=0, y=output_grid.shape[1] - 1, direction=(1, 0), color=bottom_color)
    draw_line(output_grid, x=output_grid.shape[0] - 1, y=0, direction=(0, 1), color=bottom_color)
    # Everything below the midline is bottom color, everything above is top color
    # Recolor to enforce this
    width, height = output_grid.shape
    top = output_grid[:, :height//2]
    top[top!=background] = top_color
    bottom = output_grid[:, height//2:]
    bottom[bottom!=background] = bottom_color

    return output_grid

def generate_input():
    # Generate the grid, ensure the grid has an even height so that we can split it evenly between top and bottom
    width, height = np.random.randint(10, 20, size=2)
    while (height % 2 == 1):
        width, height = np.random.randint(10, 20, size=2)
    background = Color.BLACK
    grid = np.full((width, height), background)

    # Randomly choose two colors
    colors = np.random.choice(Color.NOT_BLACK, size=2, replace=False)

    # Randomly place the pixels so that one of them is the in the bottom half and the other in the top half
    x1, x2 = np.random.choice(range(width), size=2, replace=False)
    y1, y2 = np.random.randint(2, height//2-1), np.random.randint(height//2 + 1, height-2)
    grid[x1, y1] = colors[0]
    grid[x2, y2] = colors[1]

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
