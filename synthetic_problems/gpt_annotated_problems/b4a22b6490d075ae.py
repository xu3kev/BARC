from common import *

import numpy as np
from typing import *

# concepts:
# pixel manipulation, growing, objects, collision detection

# description:
# In the input you will see a medium sized grid with individual colored pixels, some of which are green or pink (those ones are special)
# To make the output:
# 1. For each green pixel, grow a diamond shape around it until it touches another non-black pixel or the edge of the grid
# 2. For each pink pixel, grow a square shape around it until it touches another non-black pixel or the edge of the grid
# 3. If a growing shape from a green pixel touches a growing shape from a pink pixel, stop both shapes from growing further in that direction

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    
    def grow_shape(x, y, is_diamond):
        size = 1
        while True:
            grew = False
            for dx in range(-size, size + 1):
                for dy in range(-size, size + 1):
                    if is_diamond:
                        if abs(dx) + abs(dy) != size:
                            continue
                    else:
                        if abs(dx) != size and abs(dy) != size:
                            continue
                    
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < output_grid.shape[0] and 0 <= new_y < output_grid.shape[1]:
                        if output_grid[new_x, new_y] == Color.BLACK:
                            output_grid[new_x, new_y] = output_grid[x, y]
                            grew = True
                        elif output_grid[new_x, new_y] != output_grid[x, y]:
                            if (output_grid[x, y] == Color.GREEN and output_grid[new_x, new_y] == Color.PINK) or \
                               (output_grid[x, y] == Color.PINK and output_grid[new_x, new_y] == Color.GREEN):
                                return  # Stop growing if green touches pink or vice versa
            
            if not grew:
                return
            size += 1

    # First pass: grow green pixels (diamonds)
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if input_grid[x, y] == Color.GREEN:
                grow_shape(x, y, is_diamond=True)

    # Second pass: grow pink pixels (squares)
    for x in range(input_grid.shape[0]):
        for y in range(input_grid.shape[1]):
            if input_grid[x, y] == Color.PINK:
                grow_shape(x, y, is_diamond=False)

    return output_grid

def generate_input() -> np.ndarray:
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)

    num_green, num_pink, num_other = np.random.randint(1, 4), np.random.randint(1, 4), np.random.randint(1, 5)

    for _ in range(num_green):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.GREEN
    
    for _ in range(num_pink):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = Color.PINK
    
    for _ in range(num_other):
        x, y = np.random.randint(0, n), np.random.randint(0, m)
        grid[x, y] = np.random.choice([color for color in Color.NOT_BLACK if color not in [Color.GREEN, Color.PINK]])

    return grid