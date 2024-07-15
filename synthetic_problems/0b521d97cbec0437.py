from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, surrounding, uniqueness

# description:
# In the input you will see a grid with a black background and potentially multiple colored pixels.
# Exactly one color will form a symmetric pattern around a central pixel (considering horizontal, vertical, and diagonal symmetries).
# The output will be the grid with all symmetric patterns highlighted by surrounding those pixels with yellow pixels.

def main(input_grid):
    # Create an output grid initialized to black
    output_grid = np.zeros_like(input_grid)
    
    colors_with_symmetry = {}
    # Step 1: Identify the symmetric patterns and store their center positions
    for color in Color.NOT_BLACK:
        sym_indices = np.where(input_grid == color)
        for i in range(len(sym_indices[0])):
            coord = (sym_indices[0][i], sym_indices[1][i])
            # For each color, check if it forms a symmetric pattern
            if is_symmetric_pattern(input_grid, coord, color):
                if color not in colors_with_symmetry:
                    colors_with_symmetry[color] = []
                colors_with_symmetry[color].append(coord)
    
    # Step 2: Surround the symmetric patterns with yellow pixels in the output grid
    for color, coords in colors_with_symmetry.items():
        for coord in coords:
            surround_with_color(output_grid, coord[0], coord[1], Color.YELLOW, 1)
            output_grid[coord[0], coord[1]] = color

    return output_grid

def is_symmetric_pattern(grid, coord, color):
    x, y = coord
    symmetric_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for offset in symmetric_offsets:
        dx, dy = offset
        try:
            if grid[x + dx, y + dy] != color:
                return False
        except IndexError:
            return False

    return True

def surround_with_color(grid, x, y, surround_color, radius=1):
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if 0 <= x + dx < grid.shape[0] and 0 <= y + dy < grid.shape[1] and not (dx == 0 and dy == 0):
                grid[x + dx, y + dy] = surround_color

def generate_input():
    n, m = 20, 20
    grid = np.zeros((n, m), dtype=int)

    num_patterns = np.random.randint(1, 5)
    for _ in range(num_patterns):
        color = np.random.choice(Color.NOT_BLACK)
        center_x = np.random.randint(2, n-2)
        center_y = np.random.randint(2, m-2)
        symmetric_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for offset in symmetric_offsets:
            dx, dy = offset
            grid[center_x + dx, center_y + dy] = color
        grid[center_x, center_y] = color
    
    return grid