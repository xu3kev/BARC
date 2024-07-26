from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines, objects, color guide

# description:
# In the input grid, you will see a diagonal line stretching from the top-left to the bottom-right corner of a black grid.
# Each segment of the diagonal will be of a certain color.
# The output grid will be produced by mirroring each colored segment to create an "X" shape using the color as a guide.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = input_grid.copy()
    
    for i in range(input_grid.shape[0]):
        color = input_grid[i][i]
        if color != Color.BLACK:
            draw_line(output_grid, x=i, y=input_grid.shape[1] - 1 - i, length=None, color=color, direction=(-1, -1))
            draw_line(output_grid, x=i, y=input_grid.shape[1] - 1 - i, length=None, color=color, direction=(1, 1))
            draw_line(output_grid, x=input_grid.shape[0] - 1 - i, y=i, length=None, color=color, direction=(-1, -1))
            draw_line(output_grid, x=input_grid.shape[0] - 1 - i, y=i, length=None, color=color, direction=(1, 1))
    
    return output_grid

def generate_input() -> np.ndarray:
    size = np.random.randint(7, 15)
    grid = np.full((size, size), Color.BLACK, dtype=int)
    
    colors = np.random.choice(Color.NOT_BLACK, size, replace=False)
    
    for i, color in enumerate(colors):
        grid[i, i] = color
    
    return grid