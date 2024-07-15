from common import *
import numpy as np
from typing import *

# concepts:
# patterns, growing, surrounding

# description:
# In the input grid, we have pixels of various colors placed randomly on a black background. 
# To generate the output grid, grow each pixel vertically and horizontally to form a "plus" shape until it hits another colored pixel or the boundary of the grid. 
# The initial colored pixels remain unchanged.

def main(input_grid):
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Find the non-background pixel locations and their colors
    non_background_locations = np.argwhere(input_grid != Color.BLACK)

    for x, y in non_background_locations:
        color = input_grid[x, y]

        # Draw the horizontal part of the "plus" shape
        for j in range(y + 1, width):
            if output_grid[x, j] != Color.BLACK:
                break
            output_grid[x, j] = color

        for j in range(y - 1, -1, -1):
            if output_grid[x, j] != Color.BLACK:
                break
            output_grid[x, j] = color

        # Draw the vertical part of the "plus" shape
        for i in range(x + 1, height):
            if output_grid[i, y] != Color.BLACK:
                break
            output_grid[i, y] = color

        for i in range(x - 1, -1, -1):
            if output_grid[i, y] != Color.BLACK:
                break
            output_grid[i, y] = color
    
    return output_grid


def generate_input():
    # Create a grid of random size with a black background
    n = np.random.randint(6, 15)
    grid = np.full((n, n), Color.BLACK)
    
    # Randomly place a few pixels of random colors
    num_pixels = np.random.randint(5, 10)
    for _ in range(num_pixels):
        x, y = np.random.randint(0, n), np.random.randint(0, n)
        color = np.random.choice(list(Color.NOT_BLACK))
        grid[x, y] = color
    
    return grid

# Test input generation and transformation
input_grid = generate_input()
output_grid = main(input_grid)

print("Input Grid:")
print(input_grid)
print("Output Grid:")
print(output_grid)