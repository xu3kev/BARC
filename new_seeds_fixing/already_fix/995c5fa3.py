from common import *

import numpy as np
from typing import *

# concepts:
# pattern matching, color correspondence

# description:
# In the input you will see three different 4x4 patterns of gray pixels place horizonlly and seperate by black interval. 
# To make the output grid, you should find out each pattern corresponds to a color: red, teal, yellow, or green, 
# and color the corresponding row in the output grid with the corresponding color in the order from left to right.

def main(input_grid):
    # Distinguish four different pattern with different black pixels placing on the gray background.
    b, g = Color.BLACK, Color.GRAY
    red_pattern = np.array([[g, g, g, g], [g, g, g, g], [g, g, g, g], [g, g, g, g]]).transpose()
    teal_patten = np.array([[g, g, g, g], [g, b, b, g], [g, b, b, g], [g, g, g, g]]).transpose()
    yellow_pattern = np.array([[g, g, g, g], [g, g, g, g], [g, b, b, g], [g, b, b, g]]).transpose()
    green_pattern = np.array([[g, g, g, g], [b, g, g, b], [b, g, g, b], [g, g, g, g]]).transpose()

    # Detect the patterns of gray pixels with size 4x4 place horizonlly and seperate by black interval.
    detect_patterns = detect_objects(grid=input_grid, colors=[Color.GRAY], connectivity=8, monochromatic=True)

    # Get the bounding box of each pattern and crop the pattern.
    pattern_lists = []
    for pattern in detect_patterns:
        x, y, w, h = bounding_box(grid=pattern, background=Color.BLACK)
        pattern_shape = crop(grid=pattern, background=Color.BLACK)
        pattern_lists.append({'x': x, 'y': y, 'pattern': pattern_shape})
    pattern_lists = sorted(pattern_lists, key=lambda rec: rec['x'])

    # Find the corresponding color of each pattern from left to right.
    color_list = []
    for pattern in pattern_lists:
        cur_pattern = pattern['pattern']
        if np.array_equal(cur_pattern, red_pattern):
            color_list.append(Color.RED)
        elif np.array_equal(cur_pattern, teal_patten):
            color_list.append(Color.TEAL)
        elif np.array_equal(cur_pattern, yellow_pattern):
            color_list.append(Color.YELLOW)
        elif np.array_equal(cur_pattern, green_pattern):
            color_list.append(Color.GREEN)
        else:
            raise ValueError("Invalid pattern")
    square_number = len(color_list)

    # Color the corresponding row in the output grid with the corresponding color in order.
    output_grid = np.zeros((square_number,square_number), dtype=int)
    for cnt, color in enumerate(color_list):
        draw_line(grid=output_grid, color=color, x=0, y=cnt, direction=(1, 0))
    return output_grid

def generate_input():
    # There are three patterns of gray pixels with size 4x4 place horizonlly and seperate by black interval.
    square_length = 4
    square_number = 3

    # Create four different pattern by placing black pixels on the gray background.
    b, g = Color.BLACK, Color.GRAY
    red_pattern = np.array([[g, g, g, g], [g, g, g, g], [g, g, g, g], [g, g, g, g]]).transpose()
    teal_patten = np.array([[g, g, g, g], [g, b, b, g], [g, b, b, g], [g, g, g, g]]).transpose()
    yellow_pattern = np.array([[g, g, g, g], [g, g, g, g], [g, b, b, g], [g, b, b, g]]).transpose()
    green_pattern = np.array([[g, g, g, g], [b, g, g, b], [b, g, g, b], [g, g, g, g]]).transpose()
    
    # Calulate the size of the input grid.
    n = square_number * square_length + square_number - 1
    m = square_length

    grid = np.zeros((n, m), dtype=int)

    # Assign the color of each pattern.
    available_colors = [Color.RED, Color.TEAL, Color.YELLOW, Color.GREEN]

    # Randomly choose the three patterns represented by the given colors on the input grid.
    color_list = np.random.choice(available_colors, size=square_number, replace=False)
    
    # Place the corresponding pattern on the input grid.
    for square_num, color in enumerate(color_list):
        x = square_num * (square_length + 1)
        y = 0
        # Each pattern corresponds to a diffferent color: red, teal, yellow, or green.
        if color == Color.RED:
            grid = blit_sprite(grid=grid, sprite=red_pattern, x=x, y=y)
        elif color == Color.TEAL:
            grid = blit_sprite(grid=grid, sprite=teal_patten, x=x, y=y)
        elif color == Color.YELLOW:
            grid = blit_sprite(grid=grid, sprite=yellow_pattern, x=x, y=y)
        elif color == Color.GREEN:
            grid = blit_sprite(grid=grid, sprite=green_pattern, x=x, y=y)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
