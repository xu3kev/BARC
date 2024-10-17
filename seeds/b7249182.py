from common import *

import numpy as np
from typing import *

# concepts:
# growing, connecting

# description:
# In the input you will see two pixels of different colors aligned horizontally or vertically.
# To make the output, you need to connect the two pixels with two lines and a rectangle of size 4x5 in the middle.
# Half of the shape is colored with the color of the one side's pixel, and the other half with the color of the other side's pixel.

def main(input_grid):
    # Extract the two pixels from the input grid
    pixels = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)

    # Check if the two pixels are horizontally aligned
    if_horizontal = object_position(pixels[0])[1] == object_position(pixels[1])[1]
    
    # If the two pixels are not horizontally aligned, rotate the grid for easier processing
    if not if_horizontal:
        input_grid = np.rot90(input_grid)
        pixels = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)

    # Sort the two pixels by their position, from left to right, top to bottom
    pixels = sorted(pixels, key=lambda x: object_position(x)[0])
    pixels = sorted(pixels, key=lambda x: object_position(x)[1])

    # Get the position of the two pixels
    pos1 = object_position(pixels[0])
    pos2 = object_position(pixels[1])

    # If horizontal, the inner rectangle is should be 4x5
    rectangle_len, rectangle_height = 4, 5
    rectangle_pattern = np.full((rectangle_len, rectangle_height), Color.BLACK)
    output_grid = input_grid.copy()

    # Color the rectangle's border half with the left pixel's color, half with the right pixel's color
    left_color = object_colors(pixels[0])[0]
    right_color = object_colors(pixels[1])[0]

    # Draw the border of the rectangle
    draw_line(grid=rectangle_pattern, x=0, y=0, direction=(0, 1), color=left_color)
    draw_line(grid=rectangle_pattern, x=rectangle_len - 1, y=0, direction=(0, 1), color=right_color)
    rectangle_pattern[1, 0], rectangle_pattern[1, -1] = left_color, left_color
    rectangle_pattern[rectangle_len - 2, 0], rectangle_pattern[rectangle_len - 2, -1] = right_color, right_color

    # Place the rectangle in the middle of the two pixels
    middle_x = (pos1[0] + pos2[0] + 1) // 2
    middle_y = pos1[1]
    blit_sprite(grid=output_grid, sprite=rectangle_pattern, x=middle_x - rectangle_height // 2, y=middle_y - rectangle_height // 2)

    # Connect the original two pixels with the rectangle
    connect_length =( pos2[0] - pos1[0] + 1 - rectangle_len) // 2
    draw_line(grid=output_grid, x=pos1[0], y=pos1[1], end_x=pos1[0] + connect_length, end_y=pos1[1], direction=(1, 0), color=left_color)
    draw_line(grid=output_grid, x=pos2[0], y=pos2[1], end_x=pos2[0] - connect_length, end_y=pos2[1], direction=(-1, 0), color=right_color)

    # If the grid is not horizontal, rotate it back
    if not if_horizontal:
        output_grid = np.rot90(output_grid, k=3)

    return output_grid

def generate_input():
    # Generate a random background grid
    # Make sure the grid's width is greater than its height
    n, m = random.randint(15, 20), random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    # Get the color of two pixels
    colors = np.random.choice(Color.NOT_BLACK, 2, replace=False)
    color1, color2 = colors

    # Place the two pixels on the grid
    # Ensure the two pixels are horizontally, the distance between the two pixels shoule be even
    # Ensure there is a space to place a 4x5 rectangle between the two pixels
    rectangle_width, rectangle_height = 4, 5
    x1 = np.random.randint(0, n // 2, 1)
    x2 = np.random.randint(n // 2, n, 1)

    # Ensure the distance between the two pixels is even
    # Ensure there is enough space to place the rectangle
    while (x2 - x1 + 1) % 2 == 1 or (x2 - x1 + 1) < rectangle_width + 2:
        x1 = np.random.randint(0, n  // 2, 1)
        x2 = np.random.randint(n // 2, n, 1)

    # Ensure there is enough space to place the rectangle
    y = np.random.randint(rectangle_height // 2, m - rectangle_height // 2, 1)

    # Place the two pixels on the grid
    grid[x1, y] = color1
    grid[x2, y] = color2

    # Randomly rotate the whole grid
    if np.random.rand() < 0.5:
        grid = np.rot90(grid)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
