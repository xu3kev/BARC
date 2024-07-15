from common import *

import numpy as np
from typing import *

# concepts:
# vertical lines, growing, decomposition, color change

# description:
# In the input, you will see a grid with scattered rows and columns of pixels, each of a different color.
# To produce the output, extend each row of colored pixels vertically and horizontally, and change their color to TEAL if the original pixels are green or pink, and to MAROON otherwise.

def main(input_grid):
    # Prepare a blank output grid
    output_grid = np.zeros_like(input_grid)
    
    # Extract the pixels of each color
    colored_pixels = (input_grid != Color.BLACK)
    
    # Iterate over colored pixels
    for x, y in np.argwhere(colored_pixels):
        original_color = input_grid[x, y]
        
        # Determine the new color
        if original_color == Color.GREEN or original_color == Color.PINK:
            new_color = Color.TEAL
        else:
            new_color = Color.MAROON
        
        # Grow horizontally in both directions
        for new_y in range(output_grid.shape[1]):
            if output_grid[x, new_y] == Color.BLACK:
                output_grid[x, new_y] = new_color
        
        # Grow vertically in both directions
        for new_x in range(output_grid.shape[0]):
            if output_grid[new_x, y] == Color.BLACK:
                output_grid[new_x, y] = new_color
        
    return output_grid


def generate_input():
    # Create a grid of a random size
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)
    
    # Randomly place some rows and columns of colored pixels
    n_rows, n_columns = np.random.randint(1, 4), np.random.randint(1, 4)
    colors = [Color.RED, Color.GREEN, Color.BLUE, Color.PINK, Color.ORANGE]
    
    for _ in range(n_rows):
        row = np.random.randint(n)
        color = random.choice(colors)
        start, end = np.random.randint(m - 4), np.random.randint(m - 4) + 4
        grid[row, start:end] = color
    
    for _ in range(n_columns):
        column = np.random.randint(m)
        color = random.choice(colors)
        start, end = np.random.randint(n - 4), np.random.randint(n - 4) + 4
        grid[start:end, column] = color
    
    return grid