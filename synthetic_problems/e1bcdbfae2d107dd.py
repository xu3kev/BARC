from common import *

import numpy as np
from typing import *

# concepts:
# magnetism, lines, intersection

# description:
# In the input, you will see a grid with a vertical grey line in the middle, and red and blue pixels scattered on both sides.
# To make the output:
# 1. Draw horizontal lines from each red and blue pixel towards the grey line. 
#    Red lines stop at the grey line, while blue lines continue through it.
# 2. Where blue lines intersect the grey line, change the grey pixel to green.
# 3. Where blue lines intersect with red lines, draw a yellow pixel at the intersection point.

def main(input_grid):
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Find the grey line
    grey_line = np.where(output_grid == Color.GREY)[1][0]

    # Find red and blue pixels
    red_pixels = np.argwhere(output_grid == Color.RED)
    blue_pixels = np.argwhere(output_grid == Color.BLUE)

    # Draw lines from red pixels
    for x, y in red_pixels:
        if y < grey_line:
            draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(0, 1), stop_at_color=[Color.GREY])
        else:
            draw_line(output_grid, x, y, length=None, color=Color.RED, direction=(0, -1), stop_at_color=[Color.GREY])

    # Draw lines from blue pixels and mark intersections
    for x, y in blue_pixels:
        if y < grey_line:
            draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(0, 1))
            output_grid[x, grey_line] = Color.GREEN
        else:
            draw_line(output_grid, x, y, length=None, color=Color.BLUE, direction=(0, -1))
            output_grid[x, grey_line] = Color.GREEN

    # Find yellow intersection points
    for x in range(height):
        red_points = set(np.where(output_grid[x, :] == Color.RED)[0])
        blue_points = set(np.where(output_grid[x, :] == Color.BLUE)[0])
        intersections = red_points.intersection(blue_points)
        for y in intersections:
            output_grid[x, y] = Color.YELLOW

    return output_grid

def generate_input():
    height, width = random.randint(10, 15), random.randint(10, 15)
    grid = np.full((height, width), Color.BLACK)

    # Place vertical grey line
    grey_line = width // 2
    grid[:, grey_line] = Color.GREY

    # Place red and blue pixels
    for _ in range(random.randint(3, 6)):
        x = random.randint(0, height - 1)
        y = random.randint(0, grey_line - 2) if random.random() < 0.5 else random.randint(grey_line + 2, width - 1)
        grid[x, y] = random.choice([Color.RED, Color.BLUE])

    return grid