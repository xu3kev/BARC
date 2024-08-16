from common import *

import numpy as np
from typing import *

# concepts:
# counting, uniqueness, symmetry

# description:
# In the input, you will see a grid with a black background and colored pixels scattered on it. Exactly one color occurs an odd number of times.
# To make the output, find the cells whose color appears an odd number of times, and create a new grid containing only these cells.
# Then, apply horizontal mirror symmetry to this new grid, effectively doubling its width.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Plan:
    # 1. Find the color that appears an odd number of times
    # 2. Create a new grid containing only the cells with this color
    # 3. Apply horizontal mirror symmetry to the new grid

    # 1. Find the color that appears an odd number of times
    odd_color = None
    for color in Color.NOT_BLACK:
        if np.count_nonzero(input_grid == color) % 2 == 1:
            odd_color = color
            break
    
    # 2. Create a new grid containing only the cells with this color
    odd_cells = input_grid == odd_color
    x, y, width, height = bounding_box(odd_cells)
    new_grid = np.full((height, width), Color.BLACK)
    new_grid[odd_cells[y:y+height, x:x+width]] = odd_color

    # 3. Apply horizontal mirror symmetry to the new grid
    mirrored_grid = np.hstack((new_grid, np.fliplr(new_grid)))
    
    return mirrored_grid

def generate_input() -> np.ndarray:
    # make a 12x12 black grid as background
    n, m = 12, 12
    grid = np.full((n, m), Color.BLACK)

    # randomly select a color to appear an odd number of times
    odd_color = random.choice(list(Color.NOT_BLACK))

    # choose an odd number of occurrences for the odd color
    odd_occurrences = random.randrange(3, 10, 2)

    # place the odd color in random positions
    for _ in range(odd_occurrences):
        x, y = random.randint(0, n-1), random.randint(0, m-1)
        while grid[x, y] != Color.BLACK:
            x, y = random.randint(0, n-1), random.randint(0, m-1)
        grid[x, y] = odd_color

    # fill remaining positions with other colors, ensuring they appear an even number of times
    remaining_colors = [color for color in Color.NOT_BLACK if color != odd_color]
    for color in remaining_colors:
        occurrences = random.randrange(0, 7, 2)  # 0, 2, 4, or 6 occurrences
        for _ in range(occurrences):
            x, y = random.randint(0, n-1), random.randint(0, m-1)
            while grid[x, y] != Color.BLACK:
                x, y = random.randint(0, n-1), random.randint(0, m-1)
            grid[x, y] = color

    return grid