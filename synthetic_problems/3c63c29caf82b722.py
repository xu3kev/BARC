from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, lines, borders

# description:
# In the input, you will see a rectangular border made of grey pixels, with red and blue pixels scattered inside the border.
# To make the output, draw lines from each of the red and blue pixels towards the nearest border. The lines from red pixels 
# should be red, and the lines from blue pixels should be blue. These lines should stop when they hit the grey border.
# If a pixel is equidistant from two or more sides of the border, draw lines to all equidistant sides.

def main(input_grid):
    # Copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # Find the dimensions of the grid
    height, width = input_grid.shape

    # Find the red and blue pixels
    red_pixels = np.where(input_grid == Color.RED)
    blue_pixels = np.where(input_grid == Color.BLUE)

    # Function to draw lines to nearest borders
    def draw_to_nearest_borders(x, y, color):
        distances = [y, height-1-y, x, width-1-x]  # top, bottom, left, right
        min_distance = min(distances)
        
        if distances[0] == min_distance:  # top
            draw_line(output_grid, x, y, length=None, color=color, direction=(0, -1), stop_at_color=[Color.GREY])
        if distances[1] == min_distance:  # bottom
            draw_line(output_grid, x, y, length=None, color=color, direction=(0, 1), stop_at_color=[Color.GREY])
        if distances[2] == min_distance:  # left
            draw_line(output_grid, x, y, length=None, color=color, direction=(-1, 0), stop_at_color=[Color.GREY])
        if distances[3] == min_distance:  # right
            draw_line(output_grid, x, y, length=None, color=color, direction=(1, 0), stop_at_color=[Color.GREY])

    # Draw lines from red pixels
    for i in range(len(red_pixels[0])):
        y, x = red_pixels[0][i], red_pixels[1][i]
        draw_to_nearest_borders(x, y, Color.RED)

    # Draw lines from blue pixels
    for i in range(len(blue_pixels[0])):
        y, x = blue_pixels[0][i], blue_pixels[1][i]
        draw_to_nearest_borders(x, y, Color.BLUE)

    return output_grid

def generate_input():
    # Make a random sized grid (minimum 5x5, maximum 10x10)
    height = np.random.randint(5, 11)
    width = np.random.randint(5, 11)
    grid = np.zeros((height, width), dtype=int)

    # Create grey border
    grid[0, :] = Color.GREY
    grid[-1, :] = Color.GREY
    grid[:, 0] = Color.GREY
    grid[:, -1] = Color.GREY

    # Scatter red and blue pixels inside the border
    num_pixels = np.random.randint(3, (height-2)*(width-2)//2)
    for _ in range(num_pixels):
        y = np.random.randint(1, height-1)
        x = np.random.randint(1, width-1)
        color = np.random.choice([Color.RED, Color.BLUE])
        if grid[y, x] == Color.BLACK:  # Only place if the spot is empty
            grid[y, x] = color

    return grid