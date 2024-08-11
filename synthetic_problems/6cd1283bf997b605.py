from common import *
import numpy as np
from typing import *

# concepts:
# decomposition, repetition, resizing, color

# description:
# In the input, you will see a grid with a non-background colored block in the center, and multicolored rows on the edges.
# To make the output:
# 1. Identify the central block and its color.
# 2. Expand (resize) this block by a factor of two both horizontally and vertically.
# 3. Fill the grid by repeating this expanded block in a checkerboard pattern.
# 4. Retain the original multicolored edges. 

def main(input_grid):
    background_color = Color.BLACK
    
    # Copy the input grid dimensions
    grid_height, grid_width = input_grid.shape
    
    # Identify the central block
    # We assume the central block is always surrounded by a single-threaded edge of background, so we find the first non-background pixel.
    mid_height, mid_width = grid_height // 2, grid_width // 2
    central_block_color = input_grid[mid_height, mid_width]
    
    # Create the output grid which is twice the dimension of input grid.
    output_grid = np.full((grid_height * 2, grid_width * 2), background_color)
    
    # Expand the central block by a factor of two in both directions
    expanded_block = np.full((2, 2), central_block_color)
    
    # Checkboard fill the expanded block across the entire output grid
    for i in range(0, output_grid.shape[0], 4):
        for j in range(0, output_grid.shape[1], 4):
            if (i // 2 + j // 2) % 2 == 0:
                output_grid[i:i+2, j:j+2] = expanded_block
    
    # Retain the original multicolored top and side edges
    for i in range(grid_width):
        output_grid[i*2, :2] = input_grid[i, :1]

    for j in range(grid_height):
        output_grid[:2, j*2] = input_grid[:1, j]
    
    return output_grid

import random 

def generate_input():
    # Define the dimensions of the grid
    grid_size = 5
    grid = np.zeros((grid_size, grid_size), dtype=int)
    
    # Randomly place the central block color
    central_block_color = np.random.choice(list(Color.NOT_BLACK))
    grid[grid_size//2, grid_size//2] = central_block_color
    
    # Define the edge colors
    top_edge_colors = [np.random.choice(list(Color.NOT_BLACK)) for _ in range(grid_size)]
    side_edge_colors = [np.random.choice(list(Color.NOT_BLACK)) for _ in range(grid_size)]
    
    # Assign the edge colors to the top and side edges
    for i in range(grid_size):
        grid[0, i] = top_edge_colors[i]
        grid[i, 0] = side_edge_colors[i]

    return grid