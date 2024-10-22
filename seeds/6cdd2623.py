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
    
    # Get the color all on the boundary, which is the lines' color
    for color in all_color:
        all_on_boundary = all(on_boundary(x, y) for x, y in np.argwhere(input_grid==color))
        if all_on_boundary:
            line_color = color
    output_grid = np.zeros_like(input_grid)

    # Find the boundary pixels of the line_color and then draw a horizontal/vertical line to its matching pair
    for x, y in np.argwhere(input_grid == line_color):
        # Check if it's left/right edge or top/bottom edge
        if x == 0 or x == input_grid.shape[0] - 1:
            # it's left/right, so draw horizontal
            draw_line(grid=output_grid, x=x, y=y, color=line_color, direction=(1, 0))
        elif y == 0 or y == input_grid.shape[1] - 1:
            # it's top/bottom, so draw vertical
            draw_line(grid=output_grid, x=x, y=y, color=line_color, direction=(0, 1))
    
    return output_grid

def generate_input():
    # Generate the background grid with size of n x m.
    n, m = np.random.randint(12, 20), np.random.randint(12, 20)
    grid = np.zeros((n, m), dtype=int)

    # Generate random three colors on the grid.
    three_colors = random.sample(Color.NOT_BLACK, k = 3)

    scattered_colors = three_colors[:2]
    special_color = three_colors[2]

    # Two colors of pixels are scattered on the grid as noise.
    for scattered_color in scattered_colors:
        randomly_scatter_points(grid, color=scattered_color, density=0.2)

    # One color of pixels are scattered on the boundary of the grid, and only four pixels
    # They are guaranteed to form two lines.
    for _ in range(2):
        # Choose if the line is horizontal or vertical
        if_horizonal = np.random.choice([True, False])
        if if_horizonal:
            # Choose the position of the line
            pos = np.random.choice(range(1, m - 1))

            # Draw horizontal line
            grid[0, pos] = special_color
            grid[n - 1, pos] = special_color
        else:
            # Choose the position of the line
            pos = np.random.choice(range(1, n - 1))

            # Draw vertical line
            grid[pos, 0] = special_color
            grid[pos, m - 1] = special_color

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
