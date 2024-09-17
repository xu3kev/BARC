from common import *
import numpy as np
from typing import *

# concepts:
# - Extract: Extracting a central pattern from the grid.
# - Square: Identifying and handling square patterns.
# - Color: Changing the color of the extracted pattern to match the surrounding squares.

# description:
# - `main` function: Extracts a central pattern from the grid surrounded by squares and changes its color to match the surrounding squares.
# - `generate_input` function: Generates a grid with a central pattern surrounded by squares.

def main(input_grid: np.ndarray) -> np.ndarray:
    """
    Extracts the central pattern from the grid and changes its color to match the surrounding squares.

    Parameters:
    input_grid (np.ndarray): The input grid containing the central pattern and surrounding squares.

    Returns:
    np.ndarray: The extracted and color-modified pattern.
    """
    grid = np.copy(input_grid)

    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            # Check if the current cell is part of a surrounding square
            if grid[i, j] != Color.BLACK:
                x, y = i + 1, j + 1
                # Find the extent of the pattern by moving right and down
                while grid[x, j] == Color.BLACK:
                    x = x + 1
                while grid[i, y] == Color.BLACK:
                    y = y + 1
                # Extract the central pattern
                sub_matrix = grid[i + 1:x, j + 1:y]
                # Change the color of the central pattern to match the surrounding squares
                sub_matrix[sub_matrix != Color.BLACK] = grid[i, j]
                return sub_matrix

def generate_input() -> np.ndarray:
    """
    Generates a grid with a central pattern surrounded by squares.

    Returns:
    np.ndarray: The generated grid with a central pattern and surrounding squares.
    """
    n, m = random.randint(3, 10), random.randint(3, 10)
    
    # Generate a random pattern
    sprite_ = random_sprite(n, m, color_palette=[random.choice(Color.NOT_BLACK)])
    sprite = np.zeros((n + 2, m + 2), dtype=int)
    c = random.choice(Color.NOT_BLACK)
    # Set the corners of the surrounding squares
    sprite[0, 0], sprite[0, m + 1], sprite[n + 1, 0], sprite[n + 1, m + 1] = c, c, c, c
    blit_sprite(sprite, sprite_, 1, 1)
    
    # Create the grid and place the pattern in it
    lx, ly = random.randint(n + 2, 2 * n + 2), random.randint(m + 2, 2 * m + 2)
    grid = np.zeros((lx, ly), dtype=int)
    blit_sprite(grid, sprite, random.randint(0, lx - (n + 2)), random.randint(0, ly - (m + 2)))
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
