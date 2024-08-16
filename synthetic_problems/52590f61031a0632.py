from common import *

import numpy as np
from typing import *


# concepts:
# repeating pattern, translational symmetry, rotational symmetry

# description:
# In the input grid, you will see a smaller pattern repeated multiple times in a larger grid. Each instance of the pattern may be rotated by 90, 180, or 270 degrees, but the pattern remains the same.
# To make the output, identify the repeated pattern and return it in its original orientation.

def main(input_grid):
    def rotations(sprite):
        """
        Generate all rotations of a sprite (0, 90, 180, 270 degrees)
        """
        rots = [sprite, np.rot90(sprite, k=1), np.rot90(sprite, k=2), np.rot90(sprite, k=3)]
        return rots

    def find_pattern(grid):
        """
        Find the pattern repeated in the grid by checking for translational symmetry.
        """
        n, m = grid.shape
        for size in range(1, min(n, m) // 2 + 1):
            # Extract a candidate pattern and check if it tiles the grid with any rotation
            candidate_pattern = grid[:size, :size]
            if all(
                any(np.array_equal(grid[i:i + size, j:j + size], r) for r in rotations(candidate_pattern))
                for i in range(0, n, size)
                for j in range(0, m, size)
                if i + size <= n and j + size <= m
            ):
                return candidate_pattern

    pattern = find_pattern(input_grid)
    return pattern

def generate_input():
    # Create the sprite to be duplicated; pick a trio of random colors
    n = np.random.randint(2, 5)
    sprite = random_sprite(n, n, color_palette=random.sample(list(Color.NOT_BLACK),3))
    
    # Create a larger grid and fill it with rotated copies of the sprite
    large_n = n * np.random.randint(5, 8)  # larger grid roughly 5-7 times the sprite size
    large_grid = np.zeros((large_n, large_n), dtype=int)
    
    for i in range(0, large_n, n):
        for j in range(0, large_n, n):
            rotated_sprite = np.rot90(sprite, k=np.random.choice([0, 1, 2, 3]))
            blit_sprite(large_grid, rotated_sprite, i, j)
    
    return large_grid