from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, lines, boolean logical operations

# description:
# In the input, you will see a green diagonal line on a black background, with red and blue pixels scattered on either side of the line.
# To make the output, draw lines from each of the blue and red pixels. Lines from blue pixels will go away from the diagonal line, and lines from red pixels will go towards the diagonal line.
# If a line of the same color crosses another line of the same color, the part that overlaps is removed.
def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.copy(input_grid)

    def draw_and_check_overlap(output_grid, input_grid, x, y, dx, dy, color):
        cur_x, cur_y = x, y
        while 0 <= cur_x < n and 0 <= cur_y < m:
            if output_grid[cur_x, cur_y] == color:
                output_grid[cur_x, cur_y] = Color.BLACK  # Remove the overlapping part
            else:
                output_grid[cur_x, cur_y] = color
            cur_x, cur_y = cur_x + dx, cur_y + dy

    # find the green diagonal line
    green_diagonal = np.where(input_grid == Color.GREEN)
    
    # find the red and blue pixels
    red_pixels = np.where(input_grid == Color.RED)
    blue_pixels = np.where(input_grid == Color.BLUE)

    # draw lines from the red pixels toward the diagonal line
    for i in range(len(red_pixels[0])):
        x, y = red_pixels[0][i], red_pixels[1][i]
        if x < y:
            draw_and_check_overlap(output_grid, input_grid, x, y, 1, -1, Color.RED)
        else:
            draw_and_check_overlap(output_grid, input_grid, x, y, -1, 1, Color.RED)

    # draw lines from the blue pixels away from the diagonal line
    for i in range(len(blue_pixels[0])):
        x, y = blue_pixels[0][i], blue_pixels[1][i]
        if x < y:
            draw_and_check_overlap(output_grid, input_grid, x, y, -1, 1, Color.BLUE)
        else:
            draw_and_check_overlap(output_grid, input_grid, x, y, 1, -1, Color.BLUE)

    return output_grid

def generate_input():
    n, m = 10, 10
    grid = np.full((n, m), Color.BLACK)

    # make a green diagonal line from the top-left to the bottom-right
    for i in range(min(n, m)):
        grid[i, i] = Color.GREEN

    # scatter a random number of red and blue pixels on either side of the green line
    for _ in range(np.random.randint(5, 10)):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        if (x != y):  # Ensure it's not on the green diagonal
            grid[x, y] = np.random.choice([Color.RED, Color.BLUE])
    
    return grid