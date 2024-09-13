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
    # Find the position of the horizonal lines and vertical lines
    # The objects are separated by the lines
    horizontal_lines = []
    vertical_lines = []

    for x, column in enumerate(input_grid):
        if column[0] == Color.GRAY:
            vertical_lines.append(x)
    for y, item in enumerate(input_grid[0]):
        if item == Color.GRAY:
            horizontal_lines.append(y)
    
    # Get the blue grid on the upper left of the input grid
    blue_height, blue_width = horizontal_lines[0], vertical_lines[0]
    blue_grid = random_sprite(n=blue_width, m=blue_height, color_palette=[Color.BLUE], density=1.0)
    
    # Get the green grid on the lower right of the input grid
    green_height, green_width = len(input_grid) - horizontal_lines[-1], len(input_grid[0]) - vertical_lines[-1]
    green_grid = random_sprite(n=green_width, m=green_height, color_palette=[Color.GREEN], density=1.0)

    # Get the red grid on the middle of the input grid
    if len(horizontal_lines) == 2:
        red_height = horizontal_lines[1] - horizontal_lines[0] - 1
        pos_y = horizontal_lines[0] + 1
    else:
        red_height = horizontal_lines[2] - horizontal_lines[1] - 1
        pos_y = horizontal_lines[1] + 1

    if len(vertical_lines) == 2:
        red_width = vertical_lines[1] - vertical_lines[0] - 1
        pos_x = vertical_lines[0] + 1
    else:
        red_width = vertical_lines[2] - vertical_lines[1] - 1
        pos_x = vertical_lines[1] + 1
    red_grid = random_sprite(n=red_width, m=red_height, color_palette=[Color.RED], density=1.0)

    # Place the blue, green, and red grid on the input grid
    output_grid = input_grid.copy()
    output_grid = blit_sprite(grid=input_grid, sprite=blue_grid, x=0, y=0)
    output_grid = blit_sprite(grid=output_grid, sprite=green_grid, x=vertical_lines[-1] + 1, y=horizontal_lines[-1] + 1)
    output_grid = blit_sprite(grid=output_grid, sprite=red_grid, x=pos_x, y=pos_y)
            
    return output_grid

def generate_input():
    # Generate a 10x10 grid
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)

    # Get the number of horizontal and vertical lines
    line_num = [2, 4]
    vertical_line, horizontal_line = random.choice(line_num), random.choice(line_num)

    # If there are 4 lines, then the interval between the lines should be fixed sizes
    interval = [1, 1, 1, 1, 2]

    # Get the position of the lines, make sure each line does not touch each other
    if vertical_line == 2:
        pos = random.sample(range(1, n-1), 2)
        while abs(pos[1] - pos[0]) < 2:
            pos = random.sample(range(1, n-1), 2)
    else:
        random_interval = interval.copy()
        random.shuffle(random_interval)
        pos = [random_interval[0]]
        for i in range(1, vertical_line):
            pos.append(pos[-1] + random_interval[i] + 1)
    
    # Draw the vertical lines of given positions
    for cur_pos in pos:
        draw_line(grid=grid, x=cur_pos, y=0, direction=(0, 1), color=Color.GRAY)

    # Get the position of the lines, make sure each line does not touch each other
    if horizontal_line == 2:
        pos = random.sample(range(1, m-1), 2)
        while abs(pos[1] - pos[0]) < 2:
            pos = random.sample(range(1, m-1), 2)
    else:
        random_interval = interval.copy()
        random.shuffle(random_interval)
        pos = [random_interval[0]]
        for i in range(1, horizontal_line):
            pos.append(pos[-1] + random_interval[i] + 1)
    
    # Draw the horizontal lines of given positions
    for cur_pos in pos:
        draw_line(grid=grid, x=0, y=cur_pos, direction=(1, 0), color=Color.GRAY)
    
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
