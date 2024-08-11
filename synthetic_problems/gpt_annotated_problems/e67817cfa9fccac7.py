from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, lines, objects, color guide

# description:
# In the input, you will see a vertical grey line on a black background, with red and blue pixels scattered on either side of the line.
# There will also be a small yellow square object somewhere on the grid.
# To make the output:
# 1. Draw horizontal lines from each of the blue and red pixels, with lines from the red pixels going toward the grey line and lines from the blue pixels going away from the grey line. 
#    These lines should stop when they hit the grey line, the yellow square, or the edge of the grid.
# 2. For each pixel of the yellow square, draw a diagonal line in both directions (up-right and down-right if the square is left of the grey line, up-left and down-left if it's on the right).
#    These diagonal lines should be yellow and stop when they hit any other color or the edge of the grid.

def main(input_grid):
    output_grid = np.copy(input_grid)

    # Find the location of the vertical grey line
    grey_line = np.where(output_grid == Color.GREY)
    grey_line_x = np.unique(grey_line[1])[0]

    # Find the red, blue, and yellow pixels
    red_pixels = np.where(output_grid == Color.RED)
    blue_pixels = np.where(output_grid == Color.BLUE)
    yellow_pixels = np.where(output_grid == Color.YELLOW)

    # Draw lines from the red pixels toward the grey line
    for i in range(len(red_pixels[0])):
        y, x = red_pixels[0][i], red_pixels[1][i]
        if x < grey_line_x:
            draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(1, 0), stop_at_color=[Color.GREY, Color.YELLOW])
        else:
            draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(-1, 0), stop_at_color=[Color.GREY, Color.YELLOW])

    # Draw lines from the blue pixels away from the grey line
    for i in range(len(blue_pixels[0])):
        y, x = blue_pixels[0][i], blue_pixels[1][i]
        if x < grey_line_x:
            draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(-1, 0), stop_at_color=[Color.GREY, Color.YELLOW])
        else:
            draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(1, 0), stop_at_color=[Color.GREY, Color.YELLOW])

    # Draw diagonal lines from the yellow square
    for i in range(len(yellow_pixels[0])):
        y, x = yellow_pixels[0][i], yellow_pixels[1][i]
        if x < grey_line_x:
            draw_line(output_grid, x, y, length=None, color=Color.YELLOW, direction=(1, -1), stop_at_color=Color.NOT_BLACK)
            draw_line(output_grid, x, y, length=None, color=Color.YELLOW, direction=(1, 1), stop_at_color=Color.NOT_BLACK)
        else:
            draw_line(output_grid, x, y, length=None, color=Color.YELLOW, direction=(-1, -1), stop_at_color=Color.NOT_BLACK)
            draw_line(output_grid, x, y, length=None, color=Color.YELLOW, direction=(-1, 1), stop_at_color=Color.NOT_BLACK)

    return output_grid

def generate_input():
    n, m = 15, 15
    grid = np.full((n, m), Color.BLACK)

    # Create vertical grey line
    col = np.random.randint(m//3, 2*(m//3))
    grid[:, col] = Color.GREY

    # Scatter red and blue pixels
    for side in ['left', 'right']:
        if side == 'left':
            cols = range(col)
        else:
            cols = range(col+1, m)
        
        for _ in range(np.random.randint(3, 7)):
            x = np.random.choice(cols)
            y = np.random.randint(n)
            color = np.random.choice([Color.RED, Color.BLUE])
            if grid[y, x] == Color.BLACK:
                grid[y, x] = color

    # Create yellow square
    square_size = 2
    while True:
        x = np.random.randint(m - square_size)
        y = np.random.randint(n - square_size)
        if np.all(grid[y:y+square_size, x:x+square_size] == Color.BLACK):
            grid[y:y+square_size, x:x+square_size] = Color.YELLOW
            break

    return grid