from common import *

import numpy as np
from typing import *

# concepts:
# patterns, color, horizontal bars, counting

# description:
# The input grid consists of horizontal patterns represented by different colors.
# Each row will contain a single color, but the number of rows with each color can vary.
# The task is to count the number of rows of each color and perform transformations based on the counts:
# - If a color appears in one row, that row remains unchanged.
# - If a color appears in two rows, those rows should be replaced with a single row of the same color stretching the length of both rows.
# - If a color appears in three or more rows, those rows should be replaced by a single row of a different specified color (e.g., GREY).

def main(input_grid: np.ndarray) -> np.ndarray:
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)
    color_count = {}

    for i in range(n):
        row_color = input_grid[i, 0]  # all elements in the row are the same color
        if row_color in color_count:
            color_count[row_color].append(i)
        else:
            color_count[row_color] = [i]

    new_row_index = 0
    for color, rows in color_count.items():
        if len(rows) == 1:
            output_grid[new_row_index, :] = input_grid[rows[0], :]
            new_row_index += 1
        elif len(rows) == 2:
            output_grid[new_row_index, :] = color
            new_row_index += 1
        else:
            output_grid[new_row_index, :] = Color.GREY
            new_row_index += 1
    
    # Cut off unused portion of the output grid
    output_grid = output_grid[:new_row_index, :]

    return output_grid

def generate_input() -> np.ndarray:
    n = np.random.randint(5, 10)
    m = np.random.randint(5, 10)

    grid = np.zeros((n, m), dtype=int)
    colors = np.random.choice(Color.NOT_BLACK, n, replace=True)

    for i in range(n):
        grid[i, :] = colors[i]

    return grid