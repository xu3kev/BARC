from common import *

import numpy as np
from typing import *

# concepts:
# vertical lines, surrounding, borders

# description:
# In the input grid, you will see multiple colored pixels randomly scattered on a black background.
# Each colored pixel will have a vertical bar of the same color placed on it, and it will then be enclosed by a green border of thickness one pixel.

def main(input_grid):
    # Get dimensions of input grid
    n, m = input_grid.shape

    # Create a blank output grid
    output_grid = np.zeros_like(input_grid)

    # Iterate over all non-black pixels in the input grid
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    for x, y in colored_pixels:
        color = input_grid[x, y]
        
        # Draw vertical bar of the same color
        output_grid[x, :] = color

        # Draw green border around each vertical bar
        draw_line(grid=output_grid, x=max(x-1, 0), y=0, length=m, color=Color.GREEN, direction=(0,1))
        draw_line(grid=output_grid, x=min(x+1, n-1), y=0, length=m, color=Color.GREEN, direction=(0,1))
        draw_line(grid=output_grid, x=max(x-1, 0), y=0, length=3, color=Color.GREEN, direction=(1,0))
        draw_line(grid=output_grid, x=max(x-1, 0), y=m-1, length=3, color=Color.GREEN, direction=(1,0))
    
    return output_grid

def generate_input():
    # Create a black grid of random size
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    # Sprinkle some random colored pixels
    num_colors = np.random.randint(5, 10)
    for _ in range(num_colors):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        color = np.random.choice(list(Color.NOT_BLACK))
        grid[x, y] = color

    return grid