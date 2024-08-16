from common import *

import numpy as np
from typing import *

# concepts:
# color guide, pixel manipulation

# description:
# In the input, you will see a rectangular grid filled with various colored pixels and one distinct "guide color".
# For each pixel of the guide color, set the entire row and column containing that pixel to match that pixel's color in the output grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    guide_color = Color.GREEN  # We'll use green as the guide color

    rows, cols = input_grid.shape

    # Find all positions of guide_color
    guide_positions = [(x, y) for x in range(rows) for y in range(cols) if input_grid[x, y] == guide_color]

    for x, y in guide_positions:
        # Set the entire row to the guide color's original color
        output_grid[x, :] = guide_color
        # Set the entire column to the guide color's original color
        output_grid[:, y] = guide_color
        
    return output_grid

def generate_input() -> np.ndarray:
    # Define the grid size
    rows = np.random.randint(5, 15)
    cols = np.random.randint(5, 15)
    
    # Initialize an empty grid
    input_grid = np.zeros((rows, cols), dtype=int)

    # Fill the grid with random colors
    for x in range(rows):
        for y in range(cols):
            input_grid[x, y] = np.random.choice(list(Color.NOT_BLACK))

    # Place the guide color at a few random positions
    num_guides = np.random.randint(1, min(rows, cols) // 2)
    for _ in range(num_guides):
        guide_x, guide_y = np.random.randint(rows), np.random.randint(cols)
        input_grid[guide_x, guide_y] = Color.GREEN

    return input_grid