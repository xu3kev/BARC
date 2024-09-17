from common import *
import numpy as np
from typing import *

# concepts:
# rectangle detection

# description:
# In the input you will see a grid with random blue pixels on it.
# To make the output, you should find the largest rectangle area of black cells and turn it into pink.

def main(input_grid: np.ndarray) -> np.ndarray:
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
                if k - i + 1 >= 2 and mn >= 2 and lx * ly < (k - i + 1) * mn:
                    x, y, lx, ly = i, j, k - i + 1, mn

    # Create a pink sprite with the size of the largest rectangle found
    sprite = np.zeros((lx, ly), dtype=int)
    sprite.fill(Color.PINK)
    # Place the pink sprite on the grid
    blit_sprite(grid, sprite, x, y)

    return grid

def generate_input() -> np.ndarray:
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