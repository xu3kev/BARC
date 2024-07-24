from common import *

import numpy as np
from typing import *

# Concepts:
# patterns, direction, horizontal/vertical bars, collision detection

# Description:
# The input consists of an NxM grid with colored horizontal and vertical 1-pixel thick lines.
# The task is to identify the intersections of these lines and place a colored pixel at each intersection.
# The output grid will be the same as the input grid but with the intersections marked with a different color (let's use Color.PINK).

def main(input_grid):
    # Create a copy of the input to be the output grid so that we can mark intersections
    output_grid = np.copy(input_grid)

    # Get the unique colors present in the grid excluding black
    colors = list(np.unique(input_grid))
    if Color.BLACK in colors:
        colors.remove(Color.BLACK)

    # Iterate through the grid to find intersections
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if (input_grid[x, y] in colors):
                horizontal_line = False
                vertical_line = False

                # Check horizontal line
                if y > 0 and input_grid[x, y-1] == input_grid[x, y]:
                    horizontal_line = True
                if y < input_grid.shape[1] - 1 and input_grid[x, y+1] == input_grid[x, y]:
                    horizontal_line = True

                # Check vertical line
                if x > 0 and input_grid[x-1, y] == input_grid[x, y]:
                    vertical_line = True
                if x < input_grid.shape[0] - 1 and input_grid[x+1, y] == input_grid[x, y]:
                    vertical_line = True

                # If both horizontal and vertical lines are found, mark the intersection
                if horizontal_line and vertical_line:
                    output_grid[x, y] = Color.PINK

    return output_grid

def generate_input():
    # Determine the size of the grid
    n, m = random.randint(5, 20), random.randint(5, 20)

    # Create an empty grid
    grid = np.full((n, m), Color.BLACK)

    # Determine the number of lines to draw
    num_lines = random.randint(4, 10)

    # Draw horizontal and vertical lines
    for _ in range(num_lines):
        # Randomly choose color, ensuring it is not black or pink
        line_color = random.choice(list(Color.NOT_BLACK))
        while line_color == Color.PINK:
            line_color = random.choice(list(Color.NOT_BLACK))

        # Randomly choose direction (horizontal or vertical)
        direction = random.choice(['horizontal', 'vertical'])

        if direction == 'horizontal':
            row = random.randint(0, n - 1)
            col_start = random.randint(0, m - 1)
            length = random.randint(2, m - col_start)
            draw_line(grid, row, col_start, length=length, color=line_color, direction=(0, 1))
        else:
            col = random.randint(0, m - 1)
            row_start = random.randint(0, n - 1)
            length = random.randint(2, n - row_start)
            draw_line(grid, row_start, col, length=length, color=line_color, direction=(1, 0))

    return grid