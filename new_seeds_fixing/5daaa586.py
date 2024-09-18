from common import *
import numpy as np
from typing import *

# concepts:
# - Extraction: Identifying non-zero rows and columns to crop the grid.
# - Filling: Extending the color from the boundary to fill gaps.

# description:
# - `main` function: Crops the grid to remove rows and columns that only contain zeros, and then fills regions of the grid where a specific color is present, extending this color to the grid's boundaries.
# - `generate_input` function: Generates a grid with colored patterns and random black cells, ensuring that the grid contains specific patterns and gaps for testing.

def main(input_grid: np.ndarray) -> np.ndarray:
    """
    Processes the input grid by cropping rows and columns with only zeros and then extends specific colors to fill gaps in the grid.

    Parameters:
    input_grid (np.ndarray): The input grid with colored patterns and gaps.

    Returns:
    np.ndarray: The processed grid with colors extended to fill gaps.
    """
    grid = np.copy(input_grid)
    
    # Identify non-zero rows and columns
    rows = np.where(np.all(grid != 0, axis=1))[0]
    columns = np.where(np.all(grid != 0, axis=0))[0]
    
    # Determine the color to fill
    c = Color.BLACK
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i not in rows) and (j not in columns) and grid[i, j] != Color.BLACK:
                c = grid[i, j]
    
    # Crop the grid to the identified rows and columns
    grid = grid[rows[0] : rows[1] + 1, columns[0] : columns[1] + 1]
    
    # Extend the color to fill gaps
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            if grid[i, j] == c:
                if grid[0, j] == c:
                    for k in range(i):
                        grid[k, j] = c
                if grid[len(grid) - 1, j] == c:
                    for k in range(i, len(grid)):
                        grid[k, j] = c
                if grid[i, 0] == c:
                    for k in range(j):
                        grid[i, k] = c
                if grid[i, len(grid[0]) - 1] == c:
                    for k in range(j, len(grid[0])):
                        grid[i, k] = c

    return grid

def generate_input() -> np.ndarray:
    """
    Generates a grid with a specific pattern of colors and black cells for testing.

    Returns:
    np.ndarray: The generated grid with colored patterns and random black cells.
    """
    # Generate random dimensions for the grid
    f = np.random.randint(1, 11, size=3)
    g = np.random.randint(1, 11, size=3)
    n, m = np.sum(f) + 2, np.sum(g) + 2
    grid = np.zeros((n, m), dtype=int)
    
    # Generate random colors
    colors = np.random.choice(Color.NOT_BLACK, 4, replace=False)
    
    # Randomly determine orientation for placing colored patterns
    x, y = random.randint(0, 1), random.randint(0, 1)
    for i in range(4):
        u = x if (i & 1) == 0 else 1 - x
        v = y if i < 2 else 1 - y
        if u == 0:
            w = np.sum(f[:v + 1]) + v
            for j in range(m):
                grid[w, j] = colors[i]
        else:
            w = np.sum(g[:v + 1]) + v
            for j in range(n):
                grid[j, w] = colors[i]
    
    # Add random black cells to the grid
    c = random.choice(colors)
    for i in range(n):
        for j in range(m):
            if grid[i, j] == Color.BLACK and random.randint(0, 15) == 0:
                grid[i, j] = c
    
    # Ensure some specific cells are filled with the chosen color
    for i in range(3):
        x = random.randint(f[0] + 1, f[0] + f[1])
        y = random.randint(g[0] + 1, g[0] + g[1])
        grid[x, y] = c
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
