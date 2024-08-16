from common import *

import numpy as np
from typing import *

# concepts:
# occlusion, repetition, color mapping

# description:
# The input is a grid divided into four quadrants by red lines (horizontal and vertical).
# Each quadrant contains a pattern of colored pixels.
# To create the output:
# 1. Rotate each quadrant 90 degrees clockwise.
# 2. Apply a color mapping to each quadrant: 
#    Top-left: blue -> yellow, yellow -> blue
#    Top-right: green -> pink, pink -> green
#    Bottom-left: teal -> orange, orange -> teal
#    Bottom-right: gray -> maroon, maroon -> gray
# 3. Overlay the quadrants in this order: bottom-right, bottom-left, top-right, top-left.
# The red dividing lines should remain visible in the final output.

def main(input_grid):
    # Find the red dividing lines
    red_lines = np.where(input_grid == Color.RED)
    mid_x, mid_y = np.median(red_lines[0]), np.median(red_lines[1])

    # Extract quadrants
    top_left = input_grid[:int(mid_x), :int(mid_y)]
    top_right = input_grid[:int(mid_x), int(mid_y)+1:]
    bottom_left = input_grid[int(mid_x)+1:, :int(mid_y)]
    bottom_right = input_grid[int(mid_x)+1:, int(mid_y)+1:]

    # Rotate quadrants
    top_left = np.rot90(top_left, k=-1)
    top_right = np.rot90(top_right, k=-1)
    bottom_left = np.rot90(bottom_left, k=-1)
    bottom_right = np.rot90(bottom_right, k=-1)

    # Define color mappings
    color_maps = {
        'top_left': {Color.BLUE: Color.YELLOW, Color.YELLOW: Color.BLUE},
        'top_right': {Color.GREEN: Color.PINK, Color.PINK: Color.GREEN},
        'bottom_left': {Color.TEAL: Color.ORANGE, Color.ORANGE: Color.TEAL},
        'bottom_right': {Color.GRAY: Color.MAROON, Color.MAROON: Color.GRAY}
    }

    # Apply color mappings
    for quadrant, color_map in color_maps.items():
        locals()[quadrant] = np.vectorize(lambda x: color_map.get(x, x))(locals()[quadrant])

    # Create output grid
    output_grid = np.copy(input_grid)

    # Overlay quadrants
    output_grid[int(mid_x)+1:, int(mid_y)+1:] = bottom_right
    output_grid[int(mid_x)+1:, :int(mid_y)] = bottom_left
    output_grid[:int(mid_x), int(mid_y)+1:] = top_right
    output_grid[:int(mid_x), :int(mid_y)] = top_left

    return output_grid

def generate_input():
    # Create a grid with red dividing lines
    grid_size = np.random.randint(8, 12)
    grid = np.zeros((grid_size, grid_size), dtype=int)
    mid = grid_size // 2
    grid[mid, :] = Color.RED
    grid[:, mid] = Color.RED

    # Define colors for each quadrant
    quadrant_colors = [
        [Color.BLUE, Color.YELLOW],
        [Color.GREEN, Color.PINK],
        [Color.TEAL, Color.ORANGE],
        [Color.GRAY, Color.MAROON]
    ]

    # Fill quadrants with random patterns
    for i in range(2):
        for j in range(2):
            quadrant = grid[i*mid+i:(i+1)*mid, j*mid+j:(j+1)*mid]
            colors = quadrant_colors[i*2 + j]
            for _ in range(np.random.randint(5, 10)):
                x, y = np.random.randint(0, mid-1), np.random.randint(0, mid-1)
                quadrant[x, y] = np.random.choice(colors)

    return grid