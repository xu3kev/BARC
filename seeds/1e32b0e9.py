from common import *
import numpy as np
from typing import *

# concepts:
# pattern reconstruction

# description:
# In the input you will see 9 squares seperated by 4 lines. The top-left square contains the original 5x5 pattern.
# Each square contains either a small portion of pattern or remains empty.
# To make the output, you should detect the pattern on the top-left square and fill each square 
# with missing part of original pattern by the color of the line.

def main(input_grid: np.ndarray) -> np.ndarray:
    grid = np.copy(input_grid)  # Create a copy of the input grid to avoid modifying the original

    c0 = grid[5, 5]  # Color to use for filling mismatched cells

    # Iterate over each 6x6 subgrid within the 17x17 grid
    for i in range(0, 17, 6):
        for j in range(0, 17, 6):
            # Check each cell within the 5x5 pattern of the current subgrid
            for x in range(0, 5):
                for y in range(0, 5):
                    if grid[i + x, j + y] != grid[x, y]:  # If the cell does not match the top-left pattern
                        grid[i + x, j + y] = c0  # Fill the mismatched cell with color c0
    
    return grid

def generate_input() -> np.ndarray:
    n, m = 17, 17  # Size of the grid
    line = [5, 11]  # Rows and columns to fill with a specific color

    # Initialize the grid with zeros
    grid = np.zeros((n, m), dtype=int)

    # Create a 5x5 sprite pattern
    sprite = np.zeros((5, 5), dtype=int)

    # Select colors from a predefined palette
    colors = Color.NOT_BLACK.copy()
    c0 = random.choice(colors)  # Primary color for the grid
    colors.remove(c0)
    c1 = random.choice(colors)  # Secondary color for the pattern

    # Fill specific rows and columns with the primary color
    for i in line:
        for j in range(0, n):
            grid[i, j] = c0
            grid[j, i] = c0

    # Randomly generate the sprite pattern
    for i in range(0, 5):
        for j in range(0, 5):
            if random.choice([0, 1]) == 1:
                sprite[i, j] = c1

    # Randomly fill parts of the grid with the sprite pattern
    for i in range(0, n, 6):
        for j in range(0, m, 6):
            sprite_ = sprite.copy()
            for x in range(0, 5):
                for y in range(0, 5):
                    # Randomly set cells to black if they are not in the top-left corner
                    if (i != 0 or j != 0) and random.choice([0, 1]) == 0:
                        sprite_[x, y] = Color.BLACK
            blit(grid, sprite_, i, j)  # Place the sprite on the grid
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
