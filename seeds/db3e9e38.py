from common import *

import numpy as np
from typing import *

# concepts:
# pixel patterns, pyramid, color alternation

# description:
# In the input you will see a single orange line that connects to the top of the grid.
# To make the output, you should draw a pyramid pattern outward from the orange line.
# The pattern is expanded from the orange line to the left and right of the grid.
# Each line of the pattern is one cell shorter than the previous one, and the color alternates between orange and teal.

def main(input_grid):
    # Plan:
    # 1. Parse the input
    # 2. Draw the left side of the pyramid
    # 3. Draw the right side of the pyramid

    # 1. Parse the input
    # Extract the orange line from the input grid
    original_line = find_connected_components(input_grid, monochromatic=True)[0]
    original_x, original_y, width, height = bounding_box(original_line)

    # two color pattern
    color1 = Color.ORANGE
    color2 = Color.TEAL
    # Draw on top of the input
    output_grid = np.copy(input_grid)

    # Draw the pattern from the orange line and expand to left and right
    # Each line is one cell shorter than the previous one
    # The line is colored alternately between color1 and color2

    # 2. draw pattern from left to right
    cur_color = color2
    cur_height = height - 1
    for x in range(original_x + 1, output_grid.shape[0]):
        # If the height of the line is 0, stop drawing
        if cur_height <= 0:
            break
        draw_line(output_grid, x=x, y=original_y, direction=(0, 1), length=cur_height, color=cur_color)
        # pyramid pattern, each line is one pixel shorter than the previous one
        cur_height -= 1
        # colors alternate
        cur_color = color1 if cur_color == color2 else color2
    
    # 3. Then draw pattern from right to left
    cur_color = color2
    cur_height = height - 1
    for x in reversed(range(original_x)):
        # If the height of the line is 0, stop drawing
        if cur_height <= 0:
            break
        draw_line(output_grid, x=x, y=original_y, direction=(0, 1), length=cur_height, color=cur_color)
        # pyramid pattern, each line is one pixel shorter than the previous one
        cur_height -= 1
        # colors alternate
        cur_color = color1 if cur_color == color2 else color2
    
    return output_grid

def generate_input():
    # Generate the background grid
    width, height = np.random.randint(5, 10, size=2)
    grid = np.full((width, height), Color.BLACK)

    # Randomly generate one orange line connecting to the top
    # The line should be at least 4 cells long
    length = np.random.randint(3, height - 1)

    # Randomly choose one position to start the line
    x = np.random.randint(0, width)
    line_color = Color.ORANGE
    draw_line(grid=grid, x=x, y=0, direction=(0, 1), length=length, color=line_color)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
