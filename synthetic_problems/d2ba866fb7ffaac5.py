from common import *

import numpy as np
from typing import *

# concepts:
# reflecting objects, mirror symmetry

# description:
# In the input grid, you will find objects in various colors. One side of the grid is selected randomly (left, right, top, or bottom).
# Reflect all objects across the selected side such that the grid becomes symmetric about that side. Reflexion should not
# override any existing colored pixel in the grid; it should only fill in the vacant pixels.

def main(input_grid: np.ndarray) -> np.ndarray:
    n, m = input_grid.shape
    output_grid = np.copy(input_grid)

    sides = ["left", "right", "top", "bottom"]
    chosen_side = np.random.choice(sides)

    if chosen_side == "left":
        for x in range(n):
            for y in range(m//2):
                if output_grid[x, y] == Color.BLACK and output_grid[x, m - y - 1] != Color.BLACK:
                    output_grid[x, y] = output_grid[x, m - y - 1]

    elif chosen_side == "right":
        for x in range(n):
            for y in range(m//2, m):
                if output_grid[x, y] == Color.BLACK and output_grid[x, m - y - 1] != Color.BLACK:
                    output_grid[x, y] = output_grid[x, m - y - 1]

    elif chosen_side == "top":
        for x in range(n//2):
            for y in range(m):
                if output_grid[x, y] == Color.BLACK and output_grid[n - x - 1, y] != Color.BLACK:
                    output_grid[x, y] = output_grid[n - x - 1, y]

    else:  # chosen_side == "bottom"
        for x in range(n//2, n):
            for y in range(m):
                if output_grid[x, y] == Color.BLACK and output_grid[n - x - 1, y] != Color.BLACK:
                    output_grid[x, y] = output_grid[n - x - 1, y]

    return output_grid


def generate_input() -> np.ndarray:
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)
    grid = np.zeros((n, m), dtype=int)

    # Randomly place 3 to 5 colorful objects on the grid
    num_objects = np.random.randint(3, 6)
    for _ in range(num_objects):
        obj_size = np.random.randint(2, 4)
        sprite = random_sprite([obj_size], [obj_size], density=0.5, color_palette=Color.NOT_BLACK, connectivity=8)
        x, y = random_free_location_for_object(grid, sprite, background=Color.BLACK, border_size=0, padding=1)
        blit(grid, sprite, x, y, background=Color.BLACK)

    return grid