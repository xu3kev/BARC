from common import *

import numpy as np
from typing import *

# concepts:
# objects separated by lines, color correspond to position

# description:
# In the input you will see several gray lines that separate the grid into several parts.
# To make the output grid, you should color the upper left part with blue, the lower right part with green,
# and the middle part with red.

def main(input_grid):
    # Find all the black rectangles separated by gray lines
    black_rectangles = find_connected_components(grid=input_grid, connectivity=4, monochromatic=False, background=Color.GRAY)

    # Get the bounding box of each black rectangle
    rectangles_lists = []
    for rectangle in black_rectangles:
        x, y, w, h = bounding_box(grid=rectangle, background=Color.GRAY)
        rectangles_lists.append({'x': x, 'y': y, 'w': w, 'h': h})

    # Sort the rectangles by x and y position
    rectangles_lists = sorted(rectangles_lists, key=lambda rec: rec['x'])
    rectangles_lists = sorted(rectangles_lists, key=lambda rec: rec['y'])
    
    left_upper_rectangle, middle_rectangle, right_bottom_rectangle = rectangles_lists[0], rectangles_lists[len(rectangles_lists) // 2], rectangles_lists[-1]

    # Color the left upper part with blue
    blue_grid = np.full((left_upper_rectangle['w'], left_upper_rectangle['h']), Color.BLUE)

    # Color the right lower part with green
    green_grid = np.full((right_bottom_rectangle['w'], right_bottom_rectangle['h']), Color.GREEN)

    # Color the middle part with red
    red_grid = np.full((middle_rectangle['w'], middle_rectangle['h']), Color.RED)

    # Place the blue, green, and red grid on the input grid
    output_grid = input_grid.copy()
    output_grid = blit_sprite(grid=input_grid, sprite=blue_grid, x=left_upper_rectangle['x'], y=left_upper_rectangle['y'])
    output_grid = blit_sprite(grid=input_grid, sprite=green_grid, x=right_bottom_rectangle['x'], y=right_bottom_rectangle['y'])
    output_grid = blit_sprite(grid=input_grid, sprite=red_grid, x=middle_rectangle['x'], y=middle_rectangle['y'])
            
    return output_grid

def generate_input():
    # Generate a square grid as the black background
    grid_len = np.random.randint(10, 20)
    n, m = grid_len, grid_len
    grid = np.zeros((n, m), dtype=int)

    # Get the number of horizontal and vertical lines
    line_nums = [2, 4]
    line_num = np.random.choice(line_nums)

    # Generate the gray lines' positions with interval between each line to form several rectangles
    # If padding is True, the lines will be padded with 1 grid on both sides
    vertical_lines = randomly_spaced_indices(max_len=n, n_indices=line_num, border_size=1, padding=4)
    horizontal_lines = randomly_spaced_indices(max_len=m, n_indices=line_num, border_size=1, padding=2)

    # Draw the gray vertical and horizontal lines on the grid
    for vertical_line in vertical_lines:
        draw_line(grid=grid, x=vertical_line, y=0, direction=(0, 1), color=Color.GRAY)
    
    for horizontal_line in horizontal_lines:
        draw_line(grid=grid, x=0, y=horizontal_line, direction=(1, 0), color=Color.GRAY)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
