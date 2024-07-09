from common import *
import numpy as np
import random

# concepts:
# reflective symmetry

# description:
# The input grid is a 2D grid of colors. The left half of the grid contains some random colored 
# patterns, and the right half of the grid is initially black. The task is to generate the output grid 
# by mirroring the left half onto the right half along the vertical axis.

def main(input_grid):
    # Create output grid
    output_grid = np.copy(input_grid)
    
    # Get dimensions
    rows, cols = input_grid.shape
    
    # Reflect left half to right half
    for i in range(cols//2):
        output_grid[:, cols-i-1] = output_grid[:, i]
            
    return output_grid

def generate_input():
    # Generate random grid size A*B where 5 <= A <= 20, and 10 <= B <= 40 (to ensure even column count)
    rows = random.randint(5, 20)
    cols = random.randint(10, 40)
    while cols % 2 != 0:
        cols = random.randint(10, 40)
    
    # Create empty grid
    grid = np.full((rows, cols), Color.BLACK)
    
    # Fill left half with random colors, right half remains black
    for i in range(rows):
        for j in range(cols // 2):
            grid[i, j] = random.choice(list(Color.NOT_BLACK))
    
    return grid