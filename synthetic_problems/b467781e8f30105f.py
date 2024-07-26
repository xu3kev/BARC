from common import *

import numpy as np
from typing import *

# concepts:
# color mapping, collision detection

# description:
# The input is a grid with several vertical and horizontal lines made of different colors.
# To make the output, use collision detection to identify intersections of these lines and change the color of the intersections according to a color mapping.
# Additionally, all pixels in the same row or column as an intersection will be changed to the intersection's new color.

def main(input_grid):
    output_grid = input_grid.copy()
    
    # Initialize the color map for intersections
    color_map = {
        Color.RED: Color.GREEN,
        Color.BLUE: Color.YELLOW,
        Color.YELLOW: Color.BLUE,
        Color.GREEN: Color.RED,
        Color.PINK: Color.MAROON,
        Color.MAROON: Color.PINK,
        Color.GREY: Color.TEAL,
        Color.TEAL: Color.GREY,
        Color.ORANGE: Color.BLACK,
        Color.BLACK: Color.ORANGE
    }
    
    intersections = []
    h_lines = []
    v_lines = []
    
    # Identify all vertical and horizontal lines and intersections
    for i in range(len(input_grid)):
        for j in range(len(input_grid[i])):
            if i > 0 and input_grid[i, j] == input_grid[i-1, j]:
                vertical_line = (i, j)
                v_lines.append(vertical_line)
            if j > 0 and input_grid[i, j] == input_grid[i, j-1]:
                horizontal_line = (i, j)
                h_lines.append(horizontal_line)

    # Get unique intersections
    for v in v_lines:
        for h in h_lines:
            if v == h:
                intersections.append(v)

    # Apply color mapping at the intersections
    for x, y in intersections:
        new_color = color_map.get(input_grid[x, y], input_grid[x, y])
        output_grid[x, y] = new_color
        for i in range(output_grid.shape[0]):
            if output_grid[i, y] not in color_map.values():
                output_grid[i, y] = new_color
        for j in range(output_grid.shape[1]):
            if output_grid[x, j] not in color_map.values():
                output_grid[x, j] = new_color

    return output_grid

def generate_input():
    n, m = random.randint(5, 10), random.randint(5, 10)
    grid = np.full((n, m), Color.BLACK)
    
    # Create vertical and horizontal lines of random colors
    for _ in range(random.randint(2, 4)):
        color_v = random.choice(list(Color.ALL_COLORS))
        color_h = random.choice(list(Color.ALL_COLORS))
        x_v_start, x_v_end = random.randint(0, n-1), random.randint(0, n-1)
        x_h_start, x_h_end = random.randint(0, m-1), random.randint(0, m-1)
        y_v = random.randint(0, m-1)
        y_h = random.randint(0, n-1)
        
        for i in range(min(x_v_start, x_v_end), max(x_v_start, x_v_end) + 1):
            grid[i, y_v] = color_v
        for j in range(min(x_h_start, x_h_end), max(x_h_start, x_h_end) + 1):
            grid[y_h, j] = color_h
    
    return grid