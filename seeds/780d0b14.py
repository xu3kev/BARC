from common import *

import numpy as np
from typing import *

# concepts:
# downscaling

# description:
# In the input you will see a grid consisting of a chessboard pattern of different colors.
# Each color region are incomplete scattered color, separated by grid lines.
# To make the output, make a grid with one color pixel for each region of the chessboard.

def main(input_grid):
    # Get the shape of the input grid
    n, m = input_grid.shape
    # Find all horizontal and vertical lines
    # First fine all vertical lines
    vertical_lines = []
    for i in range(n):
        if np.all(input_grid[i, :] == Color.BLACK):
            vertical_lines.append(i)
    # Then find all horizontal lines
    horizontal_lines = []
    for j in range(m):
        if np.all(input_grid[:, j] == Color.BLACK):
            horizontal_lines.append(j)
    
    # Start from (0, 0)
    vertical_lines = [0] + vertical_lines
    horizontal_lines = [0] + horizontal_lines

    # use one pixel to represent the original region and create the output grid
    w, h = len(vertical_lines), len(horizontal_lines)
    output_grid = np.full((w, h), Color.BLACK) 

    # Initialize the output grid
    for i in range(len(vertical_lines)):
        for j in range(len(horizontal_lines)):
            x1 = vertical_lines[i]
            x2 = vertical_lines[i + 1] if i + 1 < len(vertical_lines) else n
            y1 = horizontal_lines[j]
            y2 = horizontal_lines[j + 1] if j + 1 < len(horizontal_lines) else m

            # Get the original region
            region = input_grid[x1:x2, y1:y2]
            # Get the color of the region
            color = object_colors(region, background=Color.BLACK)[0]
            # Use one pixel to represent the original region
            output_grid[i, j] = color

    return output_grid

def generate_input():
    # Randomly generate the grid size
    n, m = np.random.randint(20, 30), np.random.randint(20, 30)
    grid = np.full((n, m), Color.BLACK)

    # Randomly select the grid separation
    color_w, color_h = np.random.randint(2, 5), np.random.randint(2, 5)
    horizontal_separation = generate_position_has_interval(max_len=n, position_num=color_w - 1, if_padding=True)
    vertical_separation = generate_position_has_interval(max_len=m, position_num=color_h - 1, if_padding=True)

    # Iterate from the beginning of the pattern
    horizontal_separation = np.insert(horizontal_separation, 0, 0)
    vertical_separation = np.insert(vertical_separation, 0, 0)

    # Randomly select the color
    colors = np.random.choice(Color.NOT_BLACK, color_w * color_h, replace=True)

    # Assign the colors to the pattern by the separation
    for i in range(color_w):
        for j in range(color_h):
            x1 = horizontal_separation[i]
            x2 = horizontal_separation[i + 1] if i + 1 < len(horizontal_separation) else n
            y1 = vertical_separation[j]
            y2 = vertical_separation[j + 1] if j + 1 < len(vertical_separation) else m

            pattern = np.full((x2 - x1, y2 - y1), Color.BLACK)
            pattern = random_scatter_points(grid=pattern, color=colors[i * color_h + j], density=0.8)

            blit_sprite(grid=grid, sprite=pattern, x=x1, y=y1, background=Color.BLACK)

    # Draw black lines to separate the colors
    # First draw vertical lines
    for x in horizontal_separation:
        if x != 0:
            draw_line(grid=grid, x=x, y=0, direction=(0, 1), color=Color.BLACK)

    # Then draw horizontal lines
    for y in vertical_separation:
        if y != 0:
            draw_line(grid=grid, x=0, y=y, direction=(1, 0), color=Color.BLACK)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
