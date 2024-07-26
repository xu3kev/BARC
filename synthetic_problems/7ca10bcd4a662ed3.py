from common import *

import numpy as np
from typing import *

# concepts:
# color guide, positioning, patterns

# description:
# In the input, you will see a grid with a colored vertical line on the leftmost column and a colored horizontal line on the topmost row. The rest of the grid will be filled with random colors or black. 
# To make the output, for each cell not in the top row or leftmost column, copy the color from the top row in the corresponding column to the cell if the cell is not black, otherwise, copy the color from the leftmost column in the corresponding row.
  
def main(input_grid) -> np.ndarray:
    n, m = input_grid.shape

    # Get the guide colors
    top_row_colors = input_grid[0, :]
    left_col_colors = input_grid[:, 0]

    # Initialize the output grid
    output_grid = np.copy(input_grid)

    # Apply the transformation according to the color guide
    for i in range(1, n):
        for j in range(1, m):
            if input_grid[i, j] != Color.BLACK:
                output_grid[i, j] = top_row_colors[j]
            else:
                output_grid[i, j] = left_col_colors[i]

    return output_grid

def generate_input() -> np.ndarray:
    # Randomly decide dimensions of the grid
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)

    # Initialize the grid with black color
    grid = np.full((n, m), Color.BLACK)

    # Select random colors for the top row and leftmost column
    top_row_colors = [random.choice(Color.NOT_BLACK) for _ in range(m)]
    left_col_colors = [random.choice(Color.NOT_BLACK) for _ in range(n)]

    # Fill in top row and leftmost column with the selected colors
    grid[0, :] = top_row_colors
    grid[:, 0] = left_col_colors

    # Randomly fill remaining grid cells with black or a random color
    for i in range(1, n):
        for j in range(1, m):
            grid[i, j] = random.choice(list(Color.ALL_COLORS))

    return grid