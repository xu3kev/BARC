from common import *

import numpy as np
from typing import *

# concepts:
# patterns, borders, color

# description:
# In the input you will see colored pixels forming 2x2 squares on a black background.
# To make the output, draw a border around each 2x2 square with the same color as the square. Do not merge borders if multiple squares are adjacent or overlap.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    n, m = input_grid.shape

    # Loop through the grid to find 2x2 colored squares
    for i in range(n - 1):
        for j in range(m - 1):
            # Check if we have a 2x2 block of the same color (not black)
            if input_grid[i, j] != Color.BLACK and \
               input_grid[i, j] == input_grid[i+1, j] == input_grid[i, j+1] == input_grid[i+1, j+1]:
                color = input_grid[i, j]
                # Draw border around the 2x2 block
                draw_line(output_grid, i-1, j-1, length=3, color=color, direction=(1, 0)) # top border
                draw_line(output_grid, i+2, j-1, length=3, color=color, direction=(1, 0)) # bottom border
                draw_line(output_grid, i-1, j-1, length=3, color=color, direction=(0, 1)) # left border
                draw_line(output_grid, i-1, j+2, length=3, color=color, direction=(0, 1)) # right border
                
    return output_grid


def generate_input() -> np.ndarray:
    n, m = np.random.randint(6, 12), np.random.randint(6, 12)
    grid = np.zeros((n, m), dtype=int)

    # Randomly place 2x2 colored squares on the grid
    square_colors = random.sample(Color.NOT_BLACK, np.random.randint(1, 4))
    
    for color in square_colors:
        x, y = np.random.randint(0, n-1), np.random.randint(0, m-1)
        grid[x:x+2, y:y+2] = color
    
    return grid