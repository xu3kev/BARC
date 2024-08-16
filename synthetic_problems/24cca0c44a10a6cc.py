from common import *

import numpy as np
from typing import *

# concepts:
# colors, symmetry

# description:
# The input grid contains various colored pixels. To create the output grid:
# 1. Swap the red and blue colors.
# 2. Then, apply vertical symmetry to the entire grid (mirror it left-to-right).
# 3. Finally, rotate any yellow pixels by 90 degrees clockwise around the center of the grid.

def main(input_grid):
    # Step 1: Swap red and blue
    output_grid = input_grid.copy()
    output_grid[input_grid == Color.RED] = Color.BLUE
    output_grid[input_grid == Color.BLUE] = Color.RED

    # Step 2: Apply vertical symmetry
    output_grid = np.fliplr(output_grid)

    # Step 3: Rotate yellow pixels 90 degrees clockwise
    center_y, center_x = np.array(output_grid.shape) // 2
    yellow_positions = np.argwhere(output_grid == Color.YELLOW)
    
    for y, x in yellow_positions:
        # Remove the yellow pixel from its current position
        output_grid[y, x] = Color.BLACK
        
        # Calculate new position after 90-degree clockwise rotation
        dy, dx = y - center_y, x - center_x
        new_y, new_x = center_y - dx, center_x + dy
        
        # Place the yellow pixel in its new position, ensuring it's within the grid
        if 0 <= new_y < output_grid.shape[0] and 0 <= new_x < output_grid.shape[1]:
            output_grid[new_y, new_x] = Color.YELLOW

    return output_grid

def generate_input():
    # Create a random grid with various colors
    n = np.random.randint(5, 10)
    colors = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN, Color.PINK, Color.BLACK]
    input_grid = np.random.choice(colors, size=(n, n))
    return input_grid