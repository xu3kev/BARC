from common import *

import numpy as np
from typing import *

# concepts:
# surrounding, patterns, color-based operations

# description:
# In the input, you will see a grid with various colored pixels.
# For each color (except black), create a "halo" around it by surrounding all pixels of that color with pixels of the next color in the sequence:
# RED -> GREEN -> BLUE -> YELLOW -> ORANGE -> PINK -> TEAL -> MAROON -> GREY -> RED
# The halos should not overlap. If there's a conflict, the color that comes earlier in the sequence takes precedence.
# Black pixels remain unchanged and do not get a halo.

def main(input_grid):
    output_grid = np.full_like(input_grid, Color.BLACK)
    color_sequence = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.ORANGE, Color.PINK, Color.TEAL, Color.MAROON, Color.GREY]
    
    # Process colors in reverse order of the sequence to handle conflicts
    for color in reversed(color_sequence):
        next_color = color_sequence[(color_sequence.index(color) + 1) % len(color_sequence)]
        
        for i in range(len(input_grid)):
            for j in range(len(input_grid[i])):
                if input_grid[i, j] == color:
                    # Create halo around the pixel
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < len(input_grid) and 0 <= nj < len(input_grid[i]):
                                if output_grid[ni, nj] == Color.BLACK:
                                    output_grid[ni, nj] = next_color
    
    # Copy original colored pixels
    for color in color_sequence:
        output_grid[input_grid == color] = color
    
    return output_grid

def generate_input():
    grid_size = np.random.randint(10, 15)
    grid = np.full((grid_size, grid_size), Color.BLACK)
    colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.ORANGE, Color.PINK, Color.TEAL, Color.MAROON, Color.GREY]
    
    for _ in range(np.random.randint(10, 20)):
        color = np.random.choice(colors)
        x, y = np.random.randint(0, grid_size), np.random.randint(0, grid_size)
        grid[x, y] = color
    
    return grid