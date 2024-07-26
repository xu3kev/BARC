from common import *

import numpy as np
from typing import *

# concepts:
# flood fill, spatial pattern recognition, seating arrangement

# description:
# In the input, you will see a grid representing a classroom seating arrangement. Each occupied seat is marked by colorful pixels, and empty seats are black.
# Isolated students are those who are not adjacent to any other student. Surround each isolated student with a buffer of teal pixels in the output grid to maintain social distancing.

def main(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    def is_isolated(x, y):
        # Check 8 directions around (x, y)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and input_grid[nx, ny] != Color.BLACK:
                return False
        return True
    
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != Color.BLACK and is_isolated(r, c):
                # Surround with teal (buffer color)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= r + dx < rows and 0 <= c + dy < cols:
                            output_grid[r + dx, c + dy] = Color.TEAL
                output_grid[r, c] = input_grid[r, c]  # Retain the original student color

    return output_grid


def generate_input() -> np.ndarray:
    # Create an empty grid of size 10x10
    grid_size = 10
    grid = np.full((grid_size, grid_size), Color.BLACK, dtype=int)

    # Populate the grid with students (colored cells)
    num_students = np.random.randint(5, 15)  # Random number of students
    possible_colors = list(Color.NOT_BLACK)

    for _ in range(num_students):
        color = np.random.choice(possible_colors)
        x, y = np.random.randint(0, grid_size, 2)
        grid[x, y] = color

    return grid