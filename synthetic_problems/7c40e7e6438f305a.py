from common import *

import numpy as np
from typing import *

def main(input_grid: np.ndarray) -> np.ndarray:
    # Copy the input grid to the output grid initially.
    output_grid = np.copy(input_grid)

    # For each row in the grid, if there is exactly one colored pixel, fill the whole row with that color.
    for i in range(input_grid.shape[0]):
        # Get the unique colors in the row excluding black.
        unique_colors = set(input_grid[i]) - {Color.BLACK}
        if len(unique_colors) == 1:
            color = unique_colors.pop()
            output_grid[i, :] = color

    return output_grid

def generate_input() -> np.ndarray:
    # Create a black canvas of random size between 10 and 20 for both dimensions.
    rows = np.random.randint(10, 20)
    cols = np.random.randint(10, 20)
    input_grid = np.full((rows, cols), Color.BLACK, dtype=int)

    # Determine the number of rows to be filled randomly between 2 and half the number of rows.
    num_filled_rows = np.random.randint(2, rows // 2)

    for _ in range(num_filled_rows):
        # Choose a random row to fill.
        row_idx = np.random.randint(rows)
        # Choose a random column index for the color pixel.
        col_idx = np.random.randint(cols)
        # Choose a random color for the pixel.
        color = np.random.choice(list(Color.NOT_BLACK))
        input_grid[row_idx, col_idx] = color

    return input_grid