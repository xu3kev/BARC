from common import *

import numpy as np
from typing import *

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)

    # Get the top row colors
    top_row_colors = input_grid[0]

    # Find the grey line column index (last grey appearance in the row)
    grey_col_idx = np.where(input_grid == Color.GREY)[1][-1]

    # For each column, copy the color from the top row until bottom of the grid, skipping grey line
    for col in range(grey_col_idx):
        color = top_row_colors[col]
        if color != Color.BLACK:  # Only color non-black columns
            draw_line(output_grid, col, 1, length=None, color=color, direction=(0, 1))

    return output_grid

def generate_input() -> np.ndarray:

    # Decide the grid size 
    n = np.random.randint(5, 10)
    m = np.random.randint(5, 10)
    grid = np.zeros((m, n), dtype=int)

    # Select colors for the top row, excluding black
    top_row_colors = np.random.choice(list(Color.NOT_BLACK), n, replace=True)
    
    # Assign these colors to the top row
    grid[0, :] = top_row_colors

    # Define the position of the grey line
    grey_col_idx = np.random.randint(1, n)

    # Draw the grey line vertically across the picked column
    draw_line(grid, grey_col_idx, 1, length=None, color=Color.GREY, direction=(0, 1))

    return grid