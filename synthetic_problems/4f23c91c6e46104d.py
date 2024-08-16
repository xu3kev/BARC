from common import *

import numpy as np
from typing import *

# concepts:
# Symmetric Expansion, Resizing, Color

# description:
# In the input, you will see a grid with a small colored pattern anywhere on the grid.
# The transformation involves expanding this small pattern symmetrically along both the horizontal and vertical axes to create a mirroring effect.
# To make the output, identify the small pattern, calculate the half-grid size, and expand the pattern using reflection to fill the entire grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find non-black area to identify the pattern
    x, y, w, h = bounding_box(input_grid)
    pattern = crop(input_grid[x:x+w, y:y+h])

    # Double the pattern size for mirroring
    new_h, new_w = pattern.shape[0] * 2, pattern.shape[1] * 2
    output_grid = np.full((new_h, new_w), Color.BLACK)

    # Place original pattern at four quadrants to achieve symmetric expansion
    output_grid[:pattern.shape[0], :pattern.shape[1]] = pattern  # Top-left
    output_grid[:pattern.shape[0], pattern.shape[1]:] = np.fliplr(pattern)  # Top-right
    output_grid[pattern.shape[0]:, :pattern.shape[1]] = np.flipud(pattern)  # Bottom-left
    output_grid[pattern.shape[0]:, pattern.shape[1]:] = np.flipud(np.fliplr(pattern))  # Bottom-right

    return output_grid

def generate_input() -> np.ndarray:
    # Make a random size grid for the input
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)
    grid = np.full((n, m), Color.BLACK)
    
    # Create a random small pattern with random color
    pattern_n, pattern_m = np.random.randint(1, n//2), np.random.randint(1, m//2)
    pattern = random_sprite(pattern_n, pattern_m, density=0.5, color_palette=Color.NOT_BLACK)
    
    # Place the pattern randomly in the grid
    x, y = np.random.randint(0, n-pattern_n), np.random.randint(0, m-pattern_m)
    blit(grid, pattern, x, y)
    
    return grid