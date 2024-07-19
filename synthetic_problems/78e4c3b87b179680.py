from common import *

import numpy as np
from typing import *

# concepts:
# patterns, lines, occlusion

# description:
# In the input, you will see vertical bars of different colors on a black background. Some pixels in the bars might be occluded by black pixels.
# For each vertical line in the input, fill any black pixels by the color of the nearest non-black pixel above or below it in the same column.

def main(input_grid):
    # Create output grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Get dimensions
    n, m = input_grid.shape
    
    # Fill each column
    for x in range(n):
        for y in range(m):
            if input_grid[x, y] == Color.BLACK:
                # Look above
                above_color = Color.BLACK
                for k in range(y-1, -1, -1):
                    if input_grid[x, k] != Color.BLACK:
                        above_color = input_grid[x, k]
                        break
                        
                # Look below
                below_color = Color.BLACK
                for k in range(y+1, m):
                    if input_grid[x, k] != Color.BLACK:
                        below_color = input_grid[x, k]
                        break
                
                # Fill black pixels with the nearest non-black color
                if above_color != Color.BLACK:
                    output_grid[x, y] = above_color
                elif below_color != Color.BLACK:
                    output_grid[x, y] = below_color
                # If both are black, leave it as black
    
    return output_grid


def generate_input():
    # Parameters
    height = np.random.randint(10, 20)
    width = np.random.randint(5, 10)
    
    # Create a black grid
    grid = np.zeros((width, height), dtype=int)
    
    # Draw vertical colored bars
    for col in range(width):
        color = random.choice(list(Color.NOT_BLACK))
        draw_line(grid, col, 0, length=height, color=color, direction=(0, 1))
    
    # Randomly occlude some parts of the bars with black pixels
    for col in range(width):
        for row in range(height):
            if random.random() < 0.2:
                grid[col, row] = Color.BLACK

    return grid