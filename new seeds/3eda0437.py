from common import *
import numpy as np
from typing import *

# concepts:
# - This script involves working with a grid of colors and modifying it by placing a sprite on it.
# - The `main` function identifies the largest area of contiguous black cells and places a pink sprite over it.
# - The `generate_input` function creates a random grid with blue sprites and places a random pink sprite on it.

# description:
# - `main` function: Takes a grid as input, identifies the largest contiguous area of black cells, and places a pink sprite over that area.
# - `generate_input` function: Creates a random grid with blue sprites and then adds a random pink sprite to it, returning the modified grid.

def main(input_grid: np.ndarray) -> np.ndarray:
    """
    Identifies the largest contiguous area of black cells in the input grid and places a pink sprite on it.

    Parameters:
    input_grid (np.ndarray): The input grid with different color values.

    Returns:
    np.ndarray: The modified grid with a pink sprite placed over the largest contiguous area of black cells.
    """
    grid = np.copy(input_grid)  # Create a copy of the input grid to avoid modifying the original
    x, y, lx, ly = 0, 0, 0, 0  # Initialize variables to track the position and size of the largest rectangle

    # Iterate over each cell in the grid
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i, j] == Color.BLUE:
                continue  # Skip cells with blue color

            mn = len(grid)  # Initialize the minimum width of the rectangle

            # Extend the rectangle downward as long as cells are black
            for k in range(i, len(grid)):
                if grid[k, j] != Color.BLACK:
                    break
                # Extend the rectangle to the right as long as cells are black
                for l in range(j, len(grid[0]) + 1):
                    if l == len(grid[0]) or grid[k, l] != Color.BLACK:
                        mn = min(mn, l - j)  # Update the width of the rectangle
                        break
                # Update the largest rectangle found so far
                if lx * ly < (k - i + 1) * mn:
                    x, y, lx, ly = i, j, k - i + 1, mn

    # Create a pink sprite with the size of the largest rectangle found
    sprite = np.zeros((lx, ly), dtype=int)
    sprite.fill(Color.PINK)
    # Place the pink sprite on the grid
    blit_sprite(grid, sprite, x, y)

    return grid

def generate_input() -> np.ndarray:
    """
    Generates a random grid with blue sprites and places a random pink sprite on it.

    Returns:
    np.ndarray: The generated grid with a pink sprite placed on it.
    """
    m = random.randint(2, 4)  # Random number of columns
    grid = random_sprite(n=random.randint(2, 4), m=m, color_palette=[Color.BLUE])

    # Stack additional rows with blue sprites to the grid
    for cnt in range(0, 7):
        sprite = random_sprite(n=random.randint(2, 4), m=m, color_palette=[Color.BLUE])
        grid = np.vstack((grid, sprite))
    
    # Define random dimensions for the pink sprite
    lx = random.randint(int(0.25 * len(grid)), int(0.45 * len(grid)))
    ly = random.randint(int(0.5 * len(grid[0])), int(len(grid[0])))
    sprite = np.zeros((lx, ly), dtype=int)
    # Place the pink sprite at a random position in the grid
    blit_sprite(grid, sprite, random.randint(0, len(grid) - lx + 1), random.randint(0, len(grid[0]) - ly + 1), background=None)
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)