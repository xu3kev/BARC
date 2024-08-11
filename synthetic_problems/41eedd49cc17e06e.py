from common import *

import numpy as np
from typing import *
import random

# concepts:
# proximity, counting

# description:
# In the input grid, there will be multiple blue and red pixels scattered randomly. 
# For each blue pixel, count the number of red pixels in its immediate neighborhood (up to a 1-pixel radius).
# Populate the output grid with blue pixels at each position corresponding to the count of neighboring red pixels for each blue pixel. 
# Each position in the output grid indicates how many neighboring red pixels were around the corresponding blue pixel in the input grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Create an empty output grid with the same size as input grid
    output_grid = np.zeros_like(input_grid)

    # Directions for 8 possible neighboring positions around a pixel
    directions = [(-1, -1), (-1, 0), (-1, 1), 
                  (0, -1),          (0, 1), 
                  (1, -1), (1, 0), (1, 1)]
    
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if input_grid[x, y] == Color.BLUE:
                # Count the number of red neighbors
                red_neighbors = 0
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < input_grid.shape[0] and 0 <= ny < input_grid.shape[1]:
                        if input_grid[nx, ny] == Color.RED:
                            red_neighbors += 1
                
                # Place blue pixel according to the number of red neighbors counted
                if red_neighbors > 0:
                    for i in range(red_neighbors):
                        if i < output_grid.shape[0]:
                            output_grid[i, y] = Color.BLUE
    
    return output_grid

def generate_input() -> np.ndarray:
    n, m = 10, 10
    grid = np.full((n, m), Color.BLACK, dtype=int)

    # Scatter red pixels randomly on the grid
    red_pixel_count = random.randint(5, 15)
    for _ in range(red_pixel_count):
        x, y = random.randint(0, n - 1), random.randint(0, m - 1)
        grid[x, y] = Color.RED
    
    # Scatter blue pixels randomly on the grid
    blue_pixel_count = random.randint(5, 15)
    for _ in range(blue_pixel_count):
        x, y = random.randint(0, n - 1), random.randint(0, m - 1)
        grid[x, y] = Color.BLUE

    return grid