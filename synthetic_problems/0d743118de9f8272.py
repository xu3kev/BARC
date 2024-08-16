from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines, symmetry, growing

# description:
# In the input, you will see two colored pixels of different colors on a black background.
# To make the output, draw two sets of diagonal lines:
# 1. From the first colored pixel, draw diagonal lines in all four directions until they reach the edge of the grid.
# 2. From the second colored pixel, draw diagonal lines that grow outward symmetrically, 
#    stopping when they reach the first set of lines or the edge of the grid.

def main(input_grid):
    # Make output grid
    output_grid = np.copy(input_grid)
    n, m = input_grid.shape

    # Find the two colored pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    pixel1, pixel2 = colored_pixels

    # Get colors from colored pixels
    color1 = input_grid[tuple(pixel1)]
    color2 = input_grid[tuple(pixel2)]

    # Draw diagonals from first pixel
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for direction in directions:
        draw_line(output_grid, pixel1[0], pixel1[1], length=None, color=color1, direction=direction)

    # Draw growing diagonals from second pixel
    max_length = max(n, m)
    for length in range(1, max_length):
        for direction in directions:
            x = pixel2[0] + length * direction[0]
            y = pixel2[1] + length * direction[1]
            
            # Stop if we've reached the edge of the grid
            if x < 0 or x >= n or y < 0 or y >= m:
                break
            
            # Stop if we've hit a line from the first pixel
            if output_grid[x, y] == color1:
                break
            
            # Draw the pixel if it's black
            if output_grid[x, y] == Color.BLACK:
                output_grid[x, y] = color2
            else:
                break

    return output_grid

def generate_input():
    # Make a square black grid for the background
    n = m = np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # Put two randomly colored pixels at random points on the grid
    colors = random.sample(list(Color.NOT_BLACK), 2)
    
    for color in colors:
        while True:
            x, y = np.random.randint(0, n), np.random.randint(0, m)
            if grid[x, y] == Color.BLACK:
                grid[x, y] = color
                break

    return grid