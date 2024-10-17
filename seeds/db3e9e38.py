from common import *

import numpy as np
from typing import *

# concepts:
# pattern generation

# description:
# In the input you will see a single orange line that connects to the top of the grid.
# To make the output, you should draw a pattern from the orange line.
# The pattern is expanded from the orange line to the left and right of the grid.
# Each line of the pattern is one cell shorter than the previous one, and the color alternates between orange and teal.

def main(input_grid):
    # Extract the orange line from the input grid
    original_line = find_connected_components(input_grid, monochromatic=True)[0]
    x, y, w, h = bounding_box(original_line)

    # Observe the two pattern colors
    color1 = Color.ORANGE
    color2 = Color.TEAL
    output_grid = np.copy(input_grid)

    # Draw the pattern from the orange line and expand to left and right
    # Each line is one cell shorter than the previous one
    # The line is colored alternately between color1 and color2

    # First draw pattern from left to right
    cur_color = color2
    for i in range(x + 1, output_grid.shape[0]):
        # If the height of the line is 0, stop drawing
        cur_height = h - (i - x)
        if cur_height <= 0:
            break
        draw_line(output_grid, x=i, y=y, direction=(0, 1), length=cur_height, color=cur_color)
        cur_color = color1 if cur_color == color2 else color2
    
    # Then draw pattern from right to left
    cur_color = color2
    for i in reversed(range(x)):
        # If the height of the line is 0, stop drawing
        cur_height = h -  (x - i)
        if cur_height <= 0:
            break
        draw_line(output_grid, x=i, y=y, direction=(0, 1), length=cur_height, color=cur_color)
        cur_color = color1 if cur_color == color2 else color2
    
    return output_grid

def generate_input():
    # Generate the background grid
    n, m = np.random.randint(5, 10, size=2)
    grid = np.zeros((n, m), dtype=int)

    # Randomly generate one orange line connect to the top
    # The line should be at least 4 cells long
    length = np.random.randint(3, m - 1)

    # Randomly choose one position to start the line
    x = np.random.randint(0, n)
    line_color = Color.ORANGE
    draw_line(grid=grid, x=x, y=0, direction=(0, 1), length=length, color=line_color)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
