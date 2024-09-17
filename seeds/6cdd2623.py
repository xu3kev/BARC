from common import *

import numpy as np
from typing import *

# concepts:
# draw lines, detect objects

# description:
# In the input you will see three colors scattered on the grid. One color only have four pixels on the boundary of the grid.
# To make the output grid, you should connect the four pixels of the color on the boundary of the grid to make two lines.

def main(input_grid):
    # Find the used color
    all_color = np.unique(input_grid)

    # Find the color all on the boundary, which is the lines' color
    def on_boundary(x, y):
        return x == 0 or x == input_grid.shape[0] - 1 or y == 0 or y == input_grid.shape[1] - 1
    
    # Get the lines' color
    for color in all_color:
        all_on_boundary = True
        for x, column in enumerate(input_grid):
            for y, item in enumerate(column):
                if item == color and not on_boundary(x, y):
                    all_on_boundary = False
                    break 
        if all_on_boundary:
            line_color = color
    output_grid = np.zeros_like(input_grid)

    # Find out the indicator of the vertical line and draw it
    for x, column in enumerate(input_grid):
        if column[0] == line_color:
            draw_line(grid=output_grid, x=x, y=0, color=line_color, direction=(0, 1))
    
    # Find out the indicator of the horizontal line and draw it
    for y, item in enumerate(input_grid[0]):
        if item == line_color:
            draw_line(grid=output_grid, x=0, y=y, color=line_color, direction=(1, 0))
    return output_grid

def generate_input():
    # Generate the background grid with size of n x m.
    n, m = np.random.randint(12, 20), np.random.randint(12, 20)
    grid = np.zeros((n, m), dtype=int)

    # Randomly scatter color pixels on the grid.
    def random_scatter_point_on_grid(grid, color, density):
        n, m = grid.shape
        colored = 0
        # Randomly scatter density of color pixels on the grid.
        while colored < density * n * m:
            x = np.random.randint(0, n)
            y = np.random.randint(0, m)
            if grid[x, y] == Color.BLACK:
                grid[x, y] = color
                colored += 1
        return grid

    # Generate random three colors on the grid.
    three_colors = random.sample(Color.NOT_BLACK, k = 3)

    # Two colors of pixels are scattered on the grid as noise.
    for _ in range(2):
        grid = random_scatter_point_on_grid(grid=grid, color=three_colors[_], density=0.2)
    
    # One color of pixels are scattered on the boundary of the grid, and only four pixels
    # They are guaranteed to form two lines.

    for _ in range(2):
        # Choose if the line is horizontal or vertical
        if_horizonal = np.random.choice([True, False])
        if if_horizonal:
            # Choose the position of the line, make sure the line is not too close to each other
            pos = np.random.choice(range(1, m - 1))
            while grid[0, pos] == three_colors[2] or grid[0, pos - 1] == three_colors[2] or grid[0, pos + 1] == three_colors[2]:
                pos = np.random.choice(range(1, m - 1))
            # Draw horizontal line
            grid[0, pos] = three_colors[2]
            grid[n - 1, pos] = three_colors[2]
        else:
            # Choose the position of the line, make sure the line is not too close to each other
            pos = np.random.choice(range(1, n - 1))
            while grid[pos, 0] == three_colors[2] or grid[pos - 1, 0] == three_colors[2] or grid[pos + 1, 0] == three_colors[2]:
                pos = np.random.choice(range(1, m - 1))
            # Draw vertical line
            grid[pos, 0] = three_colors[2]
            grid[pos, m - 1] = three_colors[2]

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
