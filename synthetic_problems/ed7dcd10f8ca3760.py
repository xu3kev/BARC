from common import *

import numpy as np
from typing import *

# concepts:
# uniqueness, surrounding, repetition

# description:
# In the input grid, you will see several colored pixels on a black background. Exactly one color occurs only once, and all other colors occur multiple times.
# To make the output, find the cell with the unique color, and repeat it in a pattern (diagonal/diamond) around its location in the output.
# Additionally, surround it with a red color.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.zeros_like(input_grid)
    
    # 2. Find the unique color
    unique_color = None
    for color in Color.NOT_BLACK:
        if np.count_nonzero(input_grid == color) == 1:
            unique_color = color
            break
    
    # Get the coordinates of the unique cell
    unique_coords = np.argwhere(input_grid == unique_color)[0]
    x, y = unique_coords
    
    # 3. Create the pattern around the unique cell and surround it with red
    repeat_pattern = [
        (0, 0), (-1, 1), (1, 1), (-1, -1), (1, -1),
        (-2, 0), (2, 0), (0, 2), (0, -2)
    ]
    
    # Surround the unique cell with red first
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if 0 <= i < len(input_grid) and 0 <= j < len(input_grid[0]) and (i, j) != (x, y):
                output_grid[i, j] = Color.RED
    
    # Repeat unique color in pattern
    for dx, dy in repeat_pattern:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(input_grid) and 0 <= ny < len(input_grid[0]):
            output_grid[nx, ny] = unique_color
    
    # Make sure the unique cell is also included
    output_grid[x, y] = unique_color
    
    return output_grid

def generate_input() -> np.ndarray:
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)
    
    # Randomly select a unique color from Color.NOT_BLACK
    unique_color = random.choice(Color.NOT_BLACK)
    
    # Randomly choose a non-border cell for the unique color
    non_border_cells = [(i, j) for i in range(1, n-1) for j in range(1, m-1)]
    unique_cell = random.choice(non_border_cells)
    grid[unique_cell] = unique_color
    
    # Remove the unique color from the list
    remaining_colors = [color for color in Color.NOT_BLACK if color != unique_color]
    
    for remaining_color in remaining_colors:
        # Pick a random frequency but make sure that this color is not unique (does not have frequency 1)
        frequency_of_this_color = random.choice([2, 3, 4, 5, 6])
        
        for _ in range(frequency_of_this_color):
            # Randomly choose an unoccupied cell for the remaining color
            empty_cells = [(i, j) for i in range(n) for j in range(m) if grid[i][j] == Color.BLACK]
            x, y = random.choice(empty_cells)
            grid[x, y] = remaining_color
    
    return grid