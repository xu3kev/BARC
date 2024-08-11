from common import *

import numpy as np
from typing import *

# Concepts: symmetry, copying, positioning
# Description: 
# The input grid is divided into four quadrants. Each quadrant contains a random symbol pattern of the same color. 
# The output grid is created by rotating the top-left quadrant pattern to fill the other three quadrants 
# to achieve rotational symmetry (90, 180, and 270 degrees).

def main(input_grid: np.ndarray) -> np.ndarray:
    # Dimensions of the input grid
    n, m = input_grid.shape

    # Create an empty output grid of the same size
    output_grid = np.zeros_like(input_grid)

    # Calculate the dimensions of each quadrant
    quadrant_size = n // 2

    # Extract the top-left quadrant
    top_left = input_grid[:quadrant_size, :quadrant_size]

    # Fill the output grid with rotated top-left quadrant
    output_grid[:quadrant_size, :quadrant_size] = top_left  # Top-left
    output_grid[:quadrant_size, quadrant_size:] = np.rot90(top_left, 1)  # Top-right rotated 90 degrees clockwise
    output_grid[quadrant_size:, quadrant_size:] = np.rot90(top_left, 2)  # Bottom-right rotated 180 degrees
    output_grid[quadrant_size:, :quadrant_size] = np.rot90(top_left, 3)  # Bottom-left rotated 270 degrees clockwise

    return output_grid

def generate_input() -> np.ndarray:
    # Dimensions of the grid
    n = m = np.random.randint(8, 12)
    quadrant_size = n // 2
    
    # Create an empty grid
    grid = np.zeros((n, m), dtype=int)

    # Generate random patterns for each quadrant
    colors = random.sample(Color.NOT_BLACK, 4)  # Pick four different colors

    # Fill top-left quadrant with a random pattern
    top_left_pattern = random_sprite(quadrant_size, quadrant_size, density=0.5, color_palette=[colors[0]])
    grid[:quadrant_size, :quadrant_size] = top_left_pattern

    # Fill top-right quadrant with a random pattern
    top_right_pattern = random_sprite(quadrant_size, quadrant_size, density=0.5, color_palette=[colors[1]])
    grid[:quadrant_size, quadrant_size:] = top_right_pattern

    # Fill bottom-right quadrant with a random pattern
    bottom_right_pattern = random_sprite(quadrant_size, quadrant_size, density=0.5, color_palette=[colors[2]])
    grid[quadrant_size:, quadrant_size:] = bottom_right_pattern

    # Fill bottom-left quadrant with a random pattern
    bottom_left_pattern = random_sprite(quadrant_size, quadrant_size, density=0.5, color_palette=[colors[3]])
    grid[quadrant_size:, :quadrant_size] = bottom_left_pattern

    return grid