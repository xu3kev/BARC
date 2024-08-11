from common import *

import numpy as np
from typing import *

# concepts:
# Reflection, patterns, lines

# description:
# In the input, you will see a grid with a contiguous block of pixels of various colors, missed a mirror axis in either the middle row or middle column. The mirror axis will be represented by a grey line (either vertically or horizontally).
# To make the output, mirror the pixels across the grey line to create a symmetrical image. The mirrored image will also double the size of the grid by reflecting the original block of pixels on the opposite side of the mirrored axis.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Get the coordinates of the grey line
    grey_line = np.where(np.isin(input_grid, Color.GREY))
    
    if len(set(grey_line[0])) == 1:
        # Horizontal grey line (mirror across row)
        divider_row = grey_line[0][0]
        
        # Mirror the upper part below the grey line
        block = input_grid[:divider_row, :]
        mirrored_block = np.flipud(block)
        output_grid[divider_row+1:divider_row+1+block.shape[0]] = mirrored_block
    else:
        # Vertical grey line (mirror across column)
        divider_col = grey_line[1][0]
        
        # Mirror the left part to the right of the grey line
        block = input_grid[:, :divider_col]
        mirrored_block = np.fliplr(block)
        output_grid[:, divider_col+1:divider_col+1+block.shape[1]] = mirrored_block

    return output_grid

def generate_input():
    n, m = np.random.randint(6, 15), np.random.randint(6, 15)
    
    # Create a blank grid
    grid = np.zeros((n, m), dtype=int)
    
    # Random coordinates for the block
    start_x, start_y = np.random.randint(0, n//2), np.random.randint(0, m//2)
    end_x, end_y = start_x + np.random.randint(2, n//2), start_y + np.random.randint(2, m//2)
    
    # Fill block with random colors (ensure it stays within the grid)
    for i in range(start_x, min(end_x, n)):
        for j in range(start_y, min(end_y, m)):
            grid[i, j] = random.choice(list(Color.NOT_BLACK))
    
    # Add the grey mirror line
    if np.random.rand() < 0.5:
        # Horizontal mirror line
        mirror_row = np.random.randint(end_x, n)
        grid[mirror_row, :] = Color.GREY
    else:
        # Vertical mirror line
        mirror_col = np.random.randint(end_y, m)
        grid[:, mirror_col] = Color.GREY

    return grid