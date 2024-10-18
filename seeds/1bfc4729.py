from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation

# description:
# In the input you will see a grid with two pixels.
# To make the output, you should draw a pattern from the two pixels.
# step 1: draw a horizontal line from the two pixels.
# step 2: draw a border around the pattern.
# step 3: fill the top half pattern with the top half pixel color.
# step 4: fill the bottom half pattern with the bottom half pixel color.


def main(input_grid):
    # Output grid is the same size as the input grid
    output_grid = np.zeros_like(input_grid)

    # Detect the two pixels
    pixels = find_connected_components(input_grid, monochromatic=True)
    pixels.sort(key=lambda x: object_position(x)[1])

    # Pattern color
    pattern_color = Color.GRAY

    # STEP 1: Draw a horizontal line from pixels
    for pixel in pixels:
        x, y = object_position(pixel)
        draw_line(output_grid, x=0, y=y, direction=(1, 0), color=pattern_color)
    
    # STEP 2: Draw a border around the pattern
    draw_line(output_grid, x=0, y=0, direction=(1, 0), color=pattern_color)
    draw_line(output_grid, x=0, y=0, direction=(0, 1), color=pattern_color)
    draw_line(output_grid, x=0, y=output_grid.shape[1] - 1, direction=(1, 0), color=pattern_color)
    draw_line(output_grid, x=output_grid.shape[0] - 1, y=0, direction=(0, 1), color=pattern_color)

    # STEP 3: Fill the top half pattern with the top half pixel color
    top_pixel = object_colors(pixels[0])[0]
    output_grid[:, :output_grid.shape[1] // 2][output_grid[:, :output_grid.shape[1] // 2] == pattern_color] = top_pixel

    # STEP 4: Fill the bottom half pattern with the bottom half pixel color
    bottom_pixel = object_colors(pixels[1])[0]
    output_grid[:, output_grid.shape[1] // 2:][output_grid[:, output_grid.shape[1] // 2:] == pattern_color] = bottom_pixel

    return output_grid

def generate_input():
    # Generate the background grid, ensure the grid has an even number of rows
    n, m = np.random.randint(10, 20, size=2)
    while (m % 2 == 1):
        n, m = np.random.randint(10, 20, size=2)
    grid = np.zeros((n, m), dtype=int)

    line_distance = 1
    line_width = 1
    # Randomly choose two colors
    colors = np.random.choice(Color.NOT_BLACK, size=2, replace=False)

    # Randomly place the pixel on the row that will have a line
    x1, x2 = np.random.choice(range(n), size=2, replace=False)
    grid[x1, line_distance + line_width] = colors[0]
    grid[x2, -1 - (line_distance + line_width)] = colors[1]

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
