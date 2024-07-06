from common import *
import numpy as np
from typing import *

# concepts:
# Rotate patterns

# description:
# You will see a grid with a pattern marked by colored pixels.
# This pattern will be rotated 90 degrees clockwise and then placed into an output grid.
# Colors not part of the pattern will be set to the background color (black).

def main(input_grid: np.ndarray) -> np.ndarray:
    # Extract the dimensions of the input grid
    n, m = input_grid.shape

    # Create an output grid initialized with the background color (black)
    output_grid = np.full((m, n), Color.BLACK, dtype=int)

    # Rotate the pattern 90 degrees clockwise
    # This can be achieved by transposing the grid and then reversing each row
    pattern_indices = np.argwhere(input_grid != Color.BLACK)

    for x, y in pattern_indices:
        new_x = y
        new_y = n - 1 - x
        output_grid[new_x, new_y] = input_grid[x, y]

    return output_grid

def generate_input() -> np.ndarray:
    # Define grid dimensions
    n = np.random.randint(5, 10)
    m = np.random.randint(5, 10)

    # Create a black grid
    input_grid = np.full((n, m), Color.BLACK, dtype=int)

    # Define a random color palette excluding black
    colors = [color for color in Color.NOT_BLACK]

    # Randomly place some patterns using the color palette
    num_patterns = np.random.randint(5, n * m // 2)
    
    # Populate the grid with random colors
    for _ in range(num_patterns):
        x = np.random.randint(n)
        y = np.random.randint(m)
        input_grid[x, y] = np.random.choice(colors)
    
    return input_grid