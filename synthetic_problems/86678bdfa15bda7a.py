from common import *

import numpy as np
from typing import *

# concepts:
# color mapping, sliding objects, borders

# description:
# Input is a grid with colored dots scattered around and a border of a single color.
# In the output, move each dot along its column up until it contacts the border, then change the color of each dot according to a color mapping.
# border_removed_output_grid should be the border-removed output grid.

# Color mapping
color_map = {Color.RED : Color.GREEN,
             Color.BLUE : Color.ORANGE,
             Color.YELLOW : Color.PINK,
             Color.TEAL : Color.MAROON,
             Color.MAROON : Color.TEAL,
             Color.GREEN : Color.YELLOW, 
             Color.ORANGE : Color.BLUE, 
             Color.PINK : Color.RED}

def main(input_grid):
    # Copy input grid to output grid
    output_grid = np.copy(input_grid)

    # Identify the border color (assume the border is single color and consistent around the edge)
    border_color = output_grid[0][0]

    # Traverse through each column
    for col in range(1, output_grid.shape[1] - 1):  # Avoid borders
        for row in range(1, output_grid.shape[0]):  # Avoid borders
            if output_grid[row, col] in color_map:
                pixel_color = output_grid[row, col]
                new_row = row

                # Move the pixel up until it hits the border
                while new_row > 0 and output_grid[new_row - 1, col] == Color.BLACK:
                    new_row -= 1

                # Replace with new color based on color mapping
                output_grid[new_row, col] = color_map[pixel_color]
                if row != new_row:
                    # Set the old position to black
                    output_grid[row, col] = Color.BLACK

    return output_grid

def generate_input():
    # Generate grid dimensions
    n, m = np.random.randint(6, 10), np.random.randint(6, 10)
    
    # Initialize grid with BLACK color
    grid = np.full((n, m), Color.BLACK)
    
    # Draw border with a random color
    border_color = np.random.choice(list(Color.NOT_BLACK))
    draw_line(grid, x=0, y=0, length=None, color=border_color, direction=(1,0))
    draw_line(grid, x=0, y=0, length=None, color=border_color, direction=(0,1))
    draw_line(grid, x=n-1, y=0, length=None, color=border_color, direction=(0,1))
    draw_line(grid, x=0, y=m-1, length=None, color=border_color, direction=(1,0))

    # Scatter random colored dots (avoiding the border)
    for _ in range(np.random.randint(5, 10)):
        x = np.random.randint(1, n-1)
        y = np.random.randint(1, m-1)
        color = np.random.choice(list(color_map.keys()))
        grid[x, y] = color
    
    return grid