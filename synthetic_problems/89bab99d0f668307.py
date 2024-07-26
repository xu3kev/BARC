from common import *

import numpy as np
from typing import *

# Color mapping
color_map = {Color.GREEN : Color.YELLOW, 
             Color.BLUE : Color.GRAY, 
             Color.RED : Color.PINK,
             Color.TEAL : Color.MAROON,
             Color.YELLOW : Color.GREEN, 
             Color.GRAY : Color.BLUE, 
             Color.PINK : Color.RED,
             Color.MAROON : Color.TEAL             
            }

def main(input_grid):
    # Initialize output grid with the same dimensions as input grid
    output_grid = np.copy(input_grid)

    # Get the size of the quadrants
    half_rows, half_cols = input_grid.shape[0] // 2, input_grid.shape[1] // 2

    # Extract quadrants from the input grid
    top_left = input_grid[:half_rows, :half_cols]
    top_right = input_grid[:half_rows, half_cols:]
    bottom_left = input_grid[half_rows:, :half_cols]
    bottom_right = input_grid[half_rows:, half_cols:]

    # Perform color mapping on each quadrant
    top_left_mapped = np.vectorize(lambda color: color_map.get(color, color))(top_left)
    top_right_mapped = np.vectorize(lambda color: color_map.get(color, color))(top_right)
    bottom_left_mapped = np.vectorize(lambda color: color_map.get(color, color))(bottom_left)
    bottom_right_mapped = np.vectorize(lambda color: color_map.get(color, color))(bottom_right)

    # Place the mapped quadrants in their new positions
    output_grid[half_rows:, half_cols:] = top_left_mapped
    output_grid[half_rows:, :half_cols] = top_right_mapped
    output_grid[:half_rows, half_cols:] = bottom_left_mapped
    output_grid[:half_rows, :half_cols] = bottom_right_mapped

    return output_grid
    
def generate_input():
    # Create a random grid of size 6x6
    n, m = 6, 6
    grid = np.zeros((n, m), dtype=int)

    # Select random colors for each quadrant
    colors = [np.random.choice(list(Color.NOT_BLACK)) for _ in range(4)]

    # Fill each quadrant with a random pattern of the selected color
    for i in range(n // 2):
        for j in range(m // 2):
            grid[i, j] = np.random.choice([colors[0], Color.BLACK])
            grid[i, j + m // 2] = np.random.choice([colors[1], Color.BLACK])
            grid[i + n // 2, j] = np.random.choice([colors[2], Color.BLACK])
            grid[i + n // 2, j + m // 2] = np.random.choice([colors[3], Color.BLACK])

    return grid