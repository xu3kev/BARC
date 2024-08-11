from common import *

import numpy as np
from typing import *

# concepts:
# patterns, lines, color guide

# description:
# In the input, you will see a top row with a sequence of colored pixels, followed by alternating rows of single color and grey.
# To make the output, convert each grey row to match the color in the row right above them.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)

    for i in range(2, input_grid.shape[0], 2):
        color_row = output_grid[i - 1]
        output_grid[i] = color_row

    return output_grid


def generate_input() -> np.ndarray:
    # Randomly deciding the input grid dimensions
    n = np.random.randint(10, 20)
    m = np.random.randint(15, 25)
    
    # Initializing the grid
    grid = np.zeros((n, m), dtype=int)
    
    # Creating a color sequence for the top row
    colors = np.random.choice(list(Color.NOT_BLACK), size=m, replace=True)
    
    # Assigning the top row with the chosen colors
    grid[0, :] = colors
    
    # Alternating rows between a single color and grey
    for i in range(1, n):
        if i % 2 == 1:
            row_color = np.random.choice(Color.NOT_BLACK)
            grid[i, :] = row_color
        else:
            grid[i, :] = Color.GREY
    
    return grid