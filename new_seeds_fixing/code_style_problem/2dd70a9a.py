from common import *
import numpy as np
from typing import *

# concepts:
# route finding, path generation

# description:
# In the input you will see a grid with a green rectangle as start, a red rectangle as end, and several blue pixels as obstacles.
# To make the output grid, you should find the path between green and red rectangles in the following way: 
# 1. The green route expands follows the direction indicates by rectangle.
# 2. When it touch any blue pixel, it turn around to another direction to red rectangle to avoid then.

def find(grid, times, x, y, dx, dy, move):
    """
    Recursively finds a route from a starting position (x, y) while turning around obstacles and connecting to red squares.

    Parameters:
    grid (np.ndarray): The grid representing the maze with colors.
    times (int): Number of turns made so far.
    x (int): Current x-coordinate.
    y (int): Current y-coordinate.
    dx (int): Change in x-direction (direction of movement).
    dy (int): Change in y-direction (direction of movement).
    move (int): Indicates whether a move is allowed (0: no move, 1: move allowed).

    Returns:
    bool: True if a route is found, False otherwise.
    """
    # Check if the next position is within bounds
    if x + dx >= 0 and x + dx < len(grid) and y + dy >= 0 and y + dy < len(grid[0]):
        if grid[x + dx, y + dy] == Color.BLACK:
            # Move to the next position if it's black (part of the path)
            flag = find(grid, times, x + dx, y + dy, dx, dy, 1)
            if flag:
                grid[x, y] = Color.GREEN  # Mark the path if route is found
            return flag
        if move == 0:
            return False
        if times == 2:
            if grid[x + dx, y + dy] == Color.RED:
                grid[x, y] = Color.GREEN
                return True
            return False
        # Try turning right or left
        if find(grid, times + 1, x, y, dy, dx, 0):
            return True
        if find(grid, times + 1, x, y, dy * (-1), dx * (-1), 0):
            return True
        return False
    else:
        return False

def main(input_grid: np.ndarray) -> np.ndarray:
    grid = np.copy(input_grid)

    # Find the path between pairs of green squares
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i, j] != Color.GREEN:
                continue
            # Process green squares and attempt to find a path
            if i + 1 < len(grid) and grid[i + 1, j] == Color.GREEN:
                find(grid, 0, i, j, -1, 0, 0)
                find(grid, 0, i + 1, j, 1, 0, 0)
            if j + 1 < len(grid[0]) and grid[i, j + 1] == Color.GREEN:
                find(grid, 0, i, j, 0, -1, 0)
                find(grid, 0, i, j + 1, 0, 1, 0)

    return grid

def random_direction(grid, x, y, lst = 0):
    """
    Chooses a random direction for generating the path from position (x, y) while avoiding previously used directions.

    Parameters:
    grid (np.ndarray): The grid to be filled with paths and obstacles.
    x (int): Current x-coordinate.
    y (int): Current y-coordinate.
    lst (int): Last direction used (to avoid immediate backtracking).

    Returns:
    list: A list containing the number of steps, direction in x, direction in y, and the direction code.
    """
    n, m, k = len(grid), len(grid[0]), 3
    dires = []
    if x >= k and lst != 3 and lst != 1:
        dires.append([random.randint(k, x), -1, 0, 1])
    if y >= k and lst != 4 and lst != 2:
        dires.append([random.randint(k, y), 0, -1, 2])
    if n - 1 - x >= k and lst != 1 and lst != 3:
        dires.append([random.randint(k, n - 1 - x), 1, 0, 3])
    if m - 1 - y >= k and lst != 2 and lst != 4:
        dires.append([random.randint(k, m - 1 - y), 0, 1, 4])
    return random.choice(dires)

def generate_input() -> np.ndarray:
    n, m = random.randint(10, 18), random.randint(10, 18)
    grid = np.zeros((n, m), dtype=int)
    flag = np.zeros((n, m), dtype=int)

    # Simulate the path in the input grid
    sx, sy, lst = random.randint(0, n - 1), random.randint(0, m - 1), 0
    for cnt in range(0, 3):
        d = random_direction(grid, sx, sy, lst)
        for i in range(0, d[0]):
            if cnt == 0 and i < 2:
                grid[sx + i * d[1], sy + i * d[2]] = Color.GREEN
            if cnt == 2 and d[0] - i <= 2:
                grid[sx + i * d[1], sy + i * d[2]] = Color.RED
            flag[sx + i * d[1], sy + i * d[2]] = 1
        grid[sx + d[0] * d[1], sy + d[0] * d[2]] = Color.BLUE
        sx, sy, lst = sx + (d[0] - 1) * d[1], sy + (d[0] - 1) * d[2], d[3]

    # Fill remaining cells with blue obstacles
    for i in range(0, n):
        for j in range(0, m):
            if flag[i, j] == 0 and random.randint(0, 5) > 0:
                grid[i, j] = Color.BLUE
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
