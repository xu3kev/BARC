from common import *

import numpy as np
from typing import *

# concepts:
# repetition, patterns, connecting colors

# description:
# The input consists of a 3 x 3 grid with a single color pixel surrounded by black pixels. 
# To create the output, identify the color pixel and use it as a center pixel to draw concentric squares around it. 
# The output consists of concentric squares with alternating colors, starting from the color of the input pixel then alternating with black. 
# Stop expanding the pattern when the square reaches the boundary of the grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    n, m = input_grid.shape

    # Find the single color pixel
    center_colors = input_grid[input_grid != Color.BLACK]
    assert len(center_colors) == 1
    center_color = center_colors[0]
    
    center_x, center_y = np.where(input_grid == center_color)
    center_x, center_y = center_x[0], center_y[0]
    
    max_iter = min(center_x, n - 1 - center_x, center_y, m - 1 - center_y)

    for i in range(1, max_iter + 1):
        # Decide color based on current iteration
        color = center_color if i % 2 == 1 else Color.BLACK

        for offset in range(-i, i + 1):
            # Top and bottom edges
            output_grid[center_x + offset, center_y - i] = color
            output_grid[center_x + offset, center_y + i] = color
            # Left and right edges 
            output_grid[center_x - i, center_y + offset] = color
            output_grid[center_x + i, center_y + offset] = color
    
    return output_grid


def generate_input() -> np.ndarray:
    grid_size = np.random.randint(5, 10)
    grid = np.full((grid_size, grid_size), Color.BLACK)
    
    # Choose random position in the grid for center pixel
    center_x = np.random.randint(1, grid_size - 1)
    center_y = np.random.randint(1, grid_size - 1)
    
    # Choose a random color for the center pixel
    color = np.random.choice(list(Color.NOT_BLACK))
    grid[center_x, center_y] = color
    
    return grid