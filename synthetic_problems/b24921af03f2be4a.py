from common import *

import numpy as np
from typing import *

# concepts:
# counting, rectangular cells, color guide

# description:
# In the input grid, you will see a grid divided into 3x3 rectangular cells. Each cell contains some colored pixels.
# To make the output, identify the region with the maximum number of colored pixels and change the color of that region to maroon.
# Then, replace all the other region colors (keeping the cells structure) with maroon except for any black backgrounds.

def main(input_grid: np.ndarray) -> np.ndarray:
    cell_size = 3
    
    # Find the dimensions of the input grid
    n, m = input_grid.shape
    
    # Identify rectangular regions
    n_cells_x = n // cell_size
    n_cells_y = m // cell_size
    
    max_colored_pixels = 0
    max_cell = None
    
    # Calculate colored pixels in each cell
    for i in range(n_cells_x):
        for j in range(n_cells_y):
            cell = input_grid[i * cell_size:(i + 1) * cell_size, j * cell_size:(j + 1) * cell_size]
            colored_pixels_count = np.sum(cell != Color.BLACK)
            if colored_pixels_count > max_colored_pixels:
                max_colored_pixels = colored_pixels_count
                max_cell = (i, j)
    
    # Make a copy of input grid
    output_grid = np.copy(input_grid)
    
    # Change the max cell to maroon
    if max_cell is not None:
        x, y = max_cell
        output_grid[x * cell_size:(x + 1) * cell_size, y * cell_size:(y + 1) * cell_size] = Color.MAROON
    
    # Replace all other colored pixels with maroon except black backgrounds
    for i in range(n_cells_x):
        for j in range(n_cells_y):
            if (i, j) != max_cell:
                cell = output_grid[i * cell_size:(i + 1) * cell_size, j * cell_size:(j + 1) * cell_size]
                colored_pixels = cell != Color.BLACK
                cell[colored_pixels] = Color.MAROON
    
    return output_grid


def generate_input() -> np.ndarray:
    cell_size = 3
    n_cells_x = np.random.randint(3, 6)
    n_cells_y = np.random.randint(3, 6)
    
    n = cell_size * n_cells_x
    m = cell_size * n_cells_y
    
    grid = np.full((n, m), Color.BLACK)
    
    # Fill each cell with some random colored pixels
    for i in range(n_cells_x):
        for j in range(n_cells_y):
            cell = grid[i * cell_size:(i + 1) * cell_size, j * cell_size:(j + 1) * cell_size]
            num_colored_pixels = np.random.randint(1, cell_size * cell_size)
            for _ in range(num_colored_pixels):
                x, y = np.random.randint(0, cell_size, size=2)
                cell[x, y] = random.choice(list(Color.NOT_BLACK))
    
    return grid