from common import *
import numpy as np
from typing import *

# concepts:
# - Pattern extraction: Identifying and extracting rectangular patterns from the grid.
# - Color replacement: Rotating and placing extracted patterns into a grid while handling boundary issues.

# description:
# - `find`: Recursively finds the bounding box of a pattern starting from a given point.
# - `main`: Extracts a rectangular pattern from the grid, rotates it, and attempts to place it back into the grid.
# - `add_pixel`: Expands the grid if necessary to accommodate new pixels at the specified position.
# - `generate_input`: Creates a grid with random patterns and colors, ensuring space for testing.

def find(grid, flag, x, y):
    """
    Recursively finds the bounding box of a pattern starting from (x, y).

    Parameters:
    grid (np.ndarray): The input grid.
    flag (np.ndarray): A flag array to mark visited cells.
    x (int): The starting row.
    y (int): The starting column.

    Returns:
    Tuple[int, int, int, int]: The coordinates of the bounding box (left, right, height, top).
    """
    l, r, h, t = y, y, x, x
    if flag[x, y] == 1:
        return l, r, h, t
    flag[x, y] = 1
    for i in range(0, 2):
        for j in range(0, 2):
            dx, dy = i, 1 - i
            if j == 1:
                dx, dy = (-1) * dx, (-1) * dy
            if (x + dx >= 0 and x + dx < len(grid) and
                y + dy >= 0 and y + dy < len(grid[0]) and
                grid[x + dx, y + dy] != Color.BLACK):
                l_, r_, h_, t_ = find(grid, flag, x + dx, y + dy)
                l, r, h, t = min(l, l_), max(r, r_), min(h, h_), max(t, t_)
    return l, r, h, t

def main(input_grid: np.ndarray) -> np.ndarray:
    """
    Processes the input grid by extracting a pattern, rotating it, and placing it back into the grid.

    Parameters:
    input_grid (np.ndarray): The input grid with colored patterns.

    Returns:
    np.ndarray: The grid after placing the rotated pattern.
    """
    grid = np.copy(input_grid)
    flag = np.zeros((len(grid), len(grid[0])), dtype=int)
    
    # Find the initial position of the green color and the bounding box
    d = np.argwhere(grid == Color.GREEN)[0]
    x, y = d[0], d[1]
    l, r, h, t = find(grid, flag, x, y)
    sub = grid[h : t + 1, l : r + 1]
    
    # Place the sub-pattern back into the grid
    d = np.argwhere(grid == Color.RED)
    for d_ in d:
        x, y = d_[0], d_[1]
        if x >= h and x <= t and y >= l and y <= r:
            continue
        for i in range(0, 4):
            sub = np.rot90(sub, k=-1)
            D = np.argwhere(sub == Color.RED)[0]
            X, Y = D[0], D[1]
            if (0 - X + x < 0 or len(sub) - 1 - X + x >= len(grid) or
                0 - Y + y < 0 or len(sub[0]) - 1 - Y + y >= len(grid[0])):
                continue
            
            flag = True
            for j in range(len(sub)):
                for k in range(len(sub[0])):
                    sx, sy = j - X + x, k - Y + y
                    if sub[j, k] == Color.YELLOW and grid[sx, sy] != Color.YELLOW:
                        flag = False
            if flag:
                for j in range(len(sub)):
                    for k in range(len(sub[0])):
                        grid[j - X + x, k - Y + y] = sub[j, k]
                break

    return grid
    
def add_pixel(grid, x, y, dx, dy):
    """
    Expands the grid if necessary to accommodate new pixels at position (x, y).

    Parameters:
    grid (np.ndarray): The input grid.
    x (int): The x-coordinate.
    y (int): The y-coordinate.
    dx (int): The change in x.
    dy (int): The change in y.

    Returns:
    Tuple[np.ndarray, int, int, int, int]: The updated grid and adjusted coordinates.
    """
    if x + dx < 0:
        x = x + 1
        empty_row = np.zeros(len(grid[0]), dtype=int)
        grid = np.vstack([empty_row, grid])
    if x + dx >= len(grid):
        empty_row = np.zeros(len(grid[0]), dtype=int)
        grid = np.vstack([grid, empty_row])
    if y + dy < 0:
        y = y + 1
        empty_col = np.zeros((grid.shape[0], 1), dtype=int)
        grid = np.hstack([empty_col, grid])
    if y + dy >= len(grid[0]):
        empty_col = np.zeros((grid.shape[0], 1), dtype=int)
        grid = np.hstack([grid, empty_col])
    return grid, x, y, dx, dy

def generate_input() -> np.ndarray:
    """
    Generates a grid with random colored patterns and enough space for testing.

    Returns:
    np.ndarray: The generated grid with random patterns and colors.
    """
    # Create a base grid with random dimensions and a yellow sprite
    n, m = random.randint(3, 5), random.randint(3, 5)
    grid = random_sprite(n, m, color_palette=[Color.YELLOW])
    colors = [Color.RED] + [Color.BLUE] * random.randint(2, 4) + [Color.GREEN] * random.randint(2, 4)
    
    # Add random colored pixels to the grid
    for c in colors:
        while True:
            x = random.randint(0, len(grid) - 1)
            y = random.randint(0, len(grid[0]) - 1)
            if grid[x, y] != Color.BLACK:
                flag = False
                for i in range(8):
                    r = random.randint(0, 1)
                    dx, dy = r, 1 - r
                    if random.randint(0, 1) == 1:
                        dx, dy = (-1) * dx, (-1) * dy
                    if (x + dx < 0 or x + dx >= len(grid) or
                        y + dy < 0 or y + dy >= len(grid[0]) or
                        grid[x + dx, y + dy] == Color.BLACK):
                        grid, x, y, dx, dy = add_pixel(grid, x, y, dx, dy)
                        grid[x + dx, y + dy] = c
                        flag = True
                        break
                if flag:
                    break

    # Create a larger grid and place multiple patterns
    sprite = grid.copy()
    no_red = grid.copy()
    no_red[no_red == Color.BLUE] = Color.BLACK
    no_red[no_red == Color.GREEN] = Color.BLACK
    arr = np.zeros((10, 10), dtype=int)
    grid = np.zeros((10, 10), dtype=int)

    for i in range(random.randint(3, 4)):
        put = sprite.copy() if i == 0 else no_red.copy()
        put = np.rot90(put, k=-1 * random.randint(0, 3))
        while True:
            flag = False
            for j in range(20):
                x = random.randint(1, len(grid) - len(put) - 1)
                y = random.randint(1, len(grid[0]) - len(put[0]) - 1)
                sub = arr[x - 1 : x + len(put) + 1, y - 1 : y + len(put[0]) + 1]
                if np.all(sub == 0):
                    flag = True
                    blit_sprite(grid, put, x, y)
                    sub.fill(1)
                    blit_sprite(arr, sub, x - 1, y - 1)
                    break
            if not flag:
                new_grid = np.zeros((len(grid) * 2, len(grid[0]) * 2), dtype=int)
                new_arr = np.zeros((len(grid) * 2, len(grid[0]) * 2), dtype=int)
                blit_sprite(new_grid, grid, 0, 0)
                blit_sprite(new_arr, arr, 0, 0)
                grid = new_grid
                arr = new_arr
            else:
                break
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
