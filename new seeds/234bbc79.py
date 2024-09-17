from common import *
import numpy as np
from typing import *

# concepts:
# - Grid manipulation: Removing empty rows and aligning columns with gray color.
# - Pattern generation: Creating and adjusting a grid with specific color patterns.

# description:
# - `main`: Processes the grid to remove empty rows and aligns columns with gray color.
# - `generate_input`: Creates a grid with random color patterns and ensures proper alignment.

def main(input_grid: np.ndarray) -> np.ndarray:
    """
    Processes the input grid to remove empty rows and align columns with gray color.

    Parameters:
    input_grid (np.ndarray): The input grid with patterns.

    Returns:
    np.ndarray: The processed grid with aligned columns and removed empty rows.
    """
    grid = np.copy(input_grid)  # Create a copy of the input grid for processing
    assert len(grid[0]) == 3  # Ensure the grid has exactly 3 columns

    m, n = len(grid), 0  # Initialize the number of rows in the output grid and a counter for non-empty rows

    # Identify and count non-empty rows
    for i in range(m):
        flag = True
        for j in range(3):
            if grid[i, j] != Color.BLACK:
                flag = False
        if not flag:
            n += 1  # Increment the counter for non-empty rows

    output_grid = np.zeros((n, 3), dtype=int)  # Initialize the output grid with zeros (black color)
    x, lst, lsty = 0, 0, 0  # x: index for the output grid row, lst: index for the starting row of the current block, lsty: column index of gray color

    for i in range(m + 1):
        flag = True
        if i < m:
            # Check if the current row is empty
            for j in range(3):
                if grid[i, j] != Color.BLACK:
                    flag = False
        if not flag:
            # Copy non-empty rows to the output grid
            for j in range(3):
                output_grid[x, j] = grid[i, j]
            x += 1
        else:
            # Process empty rows and align columns
            c, mx, mn = 0, -1, 3
            for k in range(lst, x):
                for j in range(3):
                    if output_grid[k, j] != Color.BLACK:
                        mx = max(mx, j)
                        mn = min(mn, j)
                    if output_grid[k, j] != Color.BLACK and output_grid[k, j] != Color.GREY:
                        c = output_grid[k, j]
            if lst > 0:
                offset = 0
                # Determine the offset needed to align columns
                for k in range(-mn, 3 - mx):
                    if lsty - k >= 0 and lsty - k < 3 and output_grid[lst, lsty - k] == Color.GREY:
                        offset = k
                if offset < 0:
                    # Shift columns left if needed
                    for k in range(lst, x):
                        for j in range(3):
                            if j - offset < 3:
                                output_grid[k, j] = output_grid[k, j - offset]
                            else:
                                output_grid[k, j] = Color.BLACK
                if offset > 0:
                    # Shift columns right if needed
                    for k in range(lst, x):
                        for j in range(2, -1, -1):
                            if j - offset >= 0:
                                output_grid[k, j] = output_grid[k, j - offset]
                            else:
                                output_grid[k, j] = Color.BLACK
                output_grid[lst, lsty] = c
            # Update the column index for gray color
            for j in range(3):
                if output_grid[x - 1, j] == Color.GREY:
                    lsty = j
                    output_grid[x - 1, j] = c
            lst = x  # Update the starting row index for the next block

    return output_grid

def generate_input() -> np.ndarray:
    """
    Generates a grid with random color patterns and adjusts for proper alignment.

    Returns:
    np.ndarray: The generated grid with random patterns and adjusted alignment.
    """
    n, m = 3, 20  # Define the initial dimensions of the grid
    grid = np.zeros((n, m), dtype=int)  # Initialize the grid with zeros (black color)

    colors = Color.NOT_BLACK.copy()
    colors.remove(Color.GREY)  # Exclude gray color for pattern generation
    t = random.choice([3, 4])  # Randomly choose the number of patterns to generate
    X, Y = random.choice([0, 1, 2]), 0  # Initial starting position for the pattern
    f_h = True

    # Generate color patterns
    while t > 0:
        t -= 1
        c = random.choice(colors)  # Choose a random color for the pattern
        x, y = X, Y
        mx, mn = X, X
        f_t = True
        t_in = random.choice([3, 4])

        while t_in > 0:
            t_in -= 1
            if (not f_h and f_t) or (t_in == 0 and t > 0):
                grid[x, y] = Color.GREY  # Mark the position with gray color
            else:
                grid[x, y] = c  # Set the color at the current position
            f_t = False
            dires = [[0, 1]]  # Possible directions to extend the pattern
            if t_in > 0 and x > 0 and grid[x - 1, y] == Color.BLACK:
                dires.append([-1, 0])
            if t_in > 0 and x < 2 and grid[x + 1, y] == Color.BLACK:
                dires.append([1, 0])
            dire = random.choice(dires)  # Choose a random direction to extend the pattern
            x += dire[0]
            y += dire[1]
            mx = max(mx, x)
            mn = min(mn, x)

        if not f_h:
            dires = [0]
            # Determine possible shifts for column alignment
            for i in range(1, 3):
                if i <= mn:
                    dires.append(-i)
                if i <= 2 - mx:
                    dires.append(i)
            dire = random.choice(dires)
            if dire < 0:
                # Shift columns left
                for _x in range(3):
                    for _y in range(Y, y):
                        if _x - dire < 3:
                            grid[_x, _y] = grid[_x - dire, _y]
                        else:
                            grid[_x, _y] = Color.BLACK
            if dire > 0:
                # Shift columns right
                for _x in range(2, -1, -1):
                    for _y in range(Y, y):
                        if _x - dire >= 0:
                            grid[_x, _y] = grid[_x - dire, _y]
                        else:
                            grid[_x, _y] = Color.BLACK

        f_h = False
        X, Y = x, y + 1  # Update the starting position for the next pattern
    
    grid_ = np.zeros((n, Y - 1), dtype=int)

    for x in range(n):
        for y in range(Y - 1):
            grid_[x, y] = grid[x, y]

    return grid_.T

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
