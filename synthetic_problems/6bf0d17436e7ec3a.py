from common import *

import numpy as np
from typing import *

# concepts:
# rotation, symmetry, quadrants

# description:
# The input grid will be a square grid of random colors.
# The output will have the input pattern in the top-left quadrant,
# the pattern rotated 90 degrees clockwise in the top-right quadrant,
# the pattern rotated 180 degrees in the bottom-right quadrant,
# and the pattern rotated 270 degrees clockwise in the bottom-left quadrant.

def main(input_grid):
    n, m = input_grid.shape
    
    # Ensure grid is square for simplicity
    assert n == m
    
    # Rotate the pattern for the different quadrants
    rotated_90 = np.rot90(input_grid, k=1)
    rotated_180 = np.rot90(input_grid, k=2)
    rotated_270 = np.rot90(input_grid, k=3)
    
    # Create the output grid that will hold 4 times the input grid size
    output_grid = np.zeros((2 * n, 2 * m), dtype=int)
    
    # Place the original and rotated patterns into appropriate quadrants
    output_grid[:n, :m] = input_grid                       # Top-left
    output_grid[:n, m:2*m] = rotated_90                    # Top-right
    output_grid[n:2*n, m:2*m] = rotated_180                # Bottom-right
    output_grid[n:2*n, :m] = rotated_270                   # Bottom-left
    
    return output_grid

def generate_input():
    # Create a random square pattern of random size and colors
    size = np.random.randint(3, 6)
    grid = random_sprite(size, size, density=0.8, symmetry="not_symmetric", color_palette=Color.NOT_BLACK)
    
    return grid

# Test run to check generate_input and main function
if __name__ == '__main__':
    input_grid = generate_input()
    output_grid = main(input_grid)
    print(output_grid)