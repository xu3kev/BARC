from common import *
import numpy as np
from typing import *

# concepts:
# Pixel duplication, directional traversal

# description:
# In the input, you will see a grid with pixels from one color forming a contiguous solid block.
# To make the output, start from the leftmost non-background pixel of the block, move to the right and duplicate the pixels in subsequent columns until the end of the block is reached.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    
    # Find the color of the contiguous solid block
    block_color = None
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != Color.BLACK:
                block_color = input_grid[i, j]
                break
        if block_color is not None:
            break
            
    assert block_color is not None, "No block color found"
    
    # Find the leftmost and rightmost columns of the block
    leftmost_col = None
    rightmost_col = None
    for j in range(input_grid.shape[1]):
        if np.any(input_grid[:, j] == block_color):
            if leftmost_col is None:
                leftmost_col = j
            rightmost_col = j
            
    assert leftmost_col is not None and rightmost_col is not None, "No block columns found"
    
    # Duplicate the pixels in subsequent columns
    for j in range(leftmost_col, rightmost_col + 1):
        for i in range(input_grid.shape[0]):
            if input_grid[i, j] == block_color:
                output_grid[:, j] = block_color
                
    return output_grid

def generate_input() -> np.ndarray:
    # Decide the size of the grid
    width, height = np.random.randint(5, 10), np.random.randint(5, 10)
    
    # Create a black grid
    grid = np.zeros((width, height), dtype=int)
    
    # Choose the color of the block
    block_color = np.random.choice(Color.NOT_BLACK)
    
    # Define the size and position of the block
    block_width = np.random.randint(2, width // 2 + 1)
    block_height = np.random.randint(2, height // 2 + 1)
    start_row = np.random.randint(0, width - block_width + 1)
    start_col = np.random.randint(0, height - block_height + 1)
    
    # Fill the block with the chosen color
    grid[start_row:start_row + block_height, start_col:start_col + block_width] = block_color
    
    return grid