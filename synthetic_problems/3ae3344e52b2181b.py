from common import *

import numpy as np
from typing import *

# concepts:
# borders, objects, color guide

# description:
# In the input, you will see a black grid with a single colored pixel in one of the corners.
# To make the output, draw a border around the grid with a thickness of one pixel. The border should use the color of the corner pixel.
# Then, place a smaller object of the same color in the center of the grid. The shape of this object should be:
# - A plus sign (+) if the colored pixel was in a top corner
# - An X shape if the colored pixel was in a bottom corner

def main(input_grid):
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)
    
    # Find the color and position of the corner pixel
    corners = [(0,0), (0,m-1), (n-1,0), (n-1,m-1)]
    corner_color = None
    corner_position = None
    for x, y in corners:
        if input_grid[x, y] != Color.BLACK:
            corner_color = input_grid[x, y]
            corner_position = (x, y)
            break
    
    # Draw the border
    draw_line(grid=output_grid, x=0, y=0, length=None, color=corner_color, direction=(1,0))
    draw_line(grid=output_grid, x=n-1, y=0, length=None, color=corner_color, direction=(0,1))
    draw_line(grid=output_grid, x=0, y=0, length=None, color=corner_color, direction=(0,1))
    draw_line(grid=output_grid, x=0, y=m-1, length=None, color=corner_color, direction=(1,0))
    
    # Determine the shape and draw it in the center
    center_x, center_y = n // 2, m // 2
    if corner_position[0] == 0:  # Top corner, draw plus sign
        draw_line(grid=output_grid, x=center_x, y=center_y-1, length=3, color=corner_color, direction=(0,1))
        draw_line(grid=output_grid, x=center_x-1, y=center_y, length=3, color=corner_color, direction=(1,0))
    else:  # Bottom corner, draw X shape
        output_grid[center_x-1:center_x+2, center_y-1:center_y+2] = corner_color
        output_grid[center_x, center_y] = Color.BLACK
    
    return output_grid

def generate_input():
    # Make a rectangular black grid
    n = np.random.randint(7, 12)
    m = np.random.randint(7, 12)
    grid = np.zeros((n, m), dtype=int)
    
    # Place a colored pixel in a random corner
    corners = [(0,0), (0,m-1), (n-1,0), (n-1,m-1)]
    corner = random.choice(corners)
    color = random.choice(list(Color.NOT_BLACK))
    grid[corner] = color
    
    return grid