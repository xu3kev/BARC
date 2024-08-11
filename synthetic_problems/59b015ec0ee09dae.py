from common import *
import numpy as np
from typing import *

# concepts:
# uniqueness, cropping, surrounding, counting

# description:
# In the input grid, you will see several colored squares.
# One of the colors will occur only once in the entire grid.
# Find the cell with this unique color and crop the smallest possible grid that contains this unique color.
# In the output grid, add a border of black pixels around the cropped area to highlight it.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Plan:
    # 1. Find the unique color by counting occurrences.
    # 2. Find and extract the cell with this unique color.
    # 3. Crop the smallest possible grid that contains this unique color.
    # 4. Add a black border around the cropped grid.
    
    # Find the unique color
    unique_color = None
    for color in Color.NOT_BLACK:
        if np.count_nonzero(input_grid == color) == 1:
            unique_color = color
            break
    
    assert unique_color is not None, "There should be exactly one unique color."

    # Crop the grid to contain only the unique color
    color_mask = (input_grid == unique_color)
    bounding_x, bounding_y, bounding_width, bounding_height = bounding_box(color_mask)
    cropped_grid = input_grid[bounding_x:bounding_x + bounding_width, bounding_y:bounding_y + bounding_height]
    
    # Create a new grid with a border around the cropped grid
    bordered_grid = np.full((cropped_grid.shape[0] + 2, cropped_grid.shape[1] + 2), Color.BLACK)
    bordered_grid[1:-1, 1:-1] = cropped_grid

    return bordered_grid


def generate_input() -> np.ndarray:
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)

    unique_color = random.choice(Color.NOT_BLACK)
    non_border_cells = [(i, j) for i in range(1, n-1) for j in range(1, m-1)]
    unique_cell = random.choice(non_border_cells)
    grid[unique_cell] = unique_color

    remaining_colors = [color for color in Color.NOT_BLACK if color != unique_color]

    for remaining_color in remaining_colors:
        frequency_of_this_color = random.choice([0, 2, 3, 4, 5, 6])
        for _ in range(frequency_of_this_color):
            empty_cells = [(i, j) for i in range(n) for j in range(m) if grid[i][j] == Color.BLACK]
            if not empty_cells:
                break
            x, y = random.choice(empty_cells)
            grid[x, y] = remaining_color

    return grid