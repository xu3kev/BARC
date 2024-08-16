from common import *

import numpy as np
from typing import *

# concepts:
# Coloring diagonal pixels, repetition, growing, patterns

# description:
# Given an input grid of arbitrary size with some colored pixels on it.
# To produce the output, replicate the input grid 3 times horizontally.
# For each colored pixel, grow a diagonal line in all four diagonal directions.
# The diagonal lines should be the same color as the original pixel and should stop when they hit another colored pixel or the edge of the grid.

def main(input_grid):
    # Replicate input grid 3 times horizontally to initialize output grid
    output_grid = np.zeros((input_grid.shape[0], 3 * input_grid.shape[1]), dtype=int)
    for i in range(3):
        blit_sprite(output_grid, input_grid, 0, i * input_grid.shape[1])

    # Create diagonal directions
    diagonal_dx_dy = [(1,1), (-1,1), (1,-1), (-1,-1)]

    # Grow diagonal lines from colored pixels
    for y in range(output_grid.shape[1]):
        for x in range(output_grid.shape[0]):
            if output_grid[x,y] != Color.BLACK:
                color = output_grid[x,y]
                for dx, dy in diagonal_dx_dy:
                    cx, cy = x, y
                    while True:
                        cx, cy = cx + dx, cy + dy
                        if cx < 0 or cx >= output_grid.shape[0] or cy < 0 or cy >= output_grid.shape[1]:
                            break
                        if output_grid[cx, cy] != Color.BLACK:
                            break
                        output_grid[cx, cy] = color

    return output_grid

def generate_input():
    # Have 2 to 5 number of colored pixels in the initial grid
    n_colored_pixels = random.randint(2, 5)
    
    # Random size of input grid
    n, m = random.randint(5, 10), random.randint(5, 10)

    # Initialize grid
    grid = np.zeros((n, m), dtype=int)
  
    # Randomly place n_colored_pixels pixels on the grid
    for _ in range(n_colored_pixels):
        color = random.choice(list(Color.NOT_BLACK))
        sprite = np.array([color]).reshape(1, 1)
        x, y = random_free_location_for_sprite(grid, sprite)
        blit_sprite(grid, sprite, x, y)

    return grid