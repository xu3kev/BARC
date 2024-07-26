from common import *

import numpy as np
from typing import *

def main(input_grid):
    height, width = input_grid.shape
    output_grid = np.zeros((height * width, height * width), dtype=int)

    red_pattern = np.zeros((1, width), dtype=int)
    red_pattern[0, :] = Color.RED

    blue_pattern = np.zeros((height, 1), dtype=int)
    blue_pattern[:, 0] = Color.BLUE

    green_pattern = np.zeros((height, width), dtype=int)
    green_pattern[:, width // 2] = Color.GREEN
    green_pattern[height // 2, :] = Color.GREEN

    for i in range(height):
        for j in range(width):
            color = input_grid[i, j]
            if color == Color.RED:
                blit_sprite(output_grid, red_pattern, x=i * height, y=j * width)
            elif color == Color.BLUE:
                blit_sprite(output_grid, blue_pattern, x=i * height, y=j * width)
            elif color == Color.GREEN:
                blit_sprite(output_grid, green_pattern, x=i * height, y=j * width)

    return output_grid

def generate_input():
    n, m = np.random.randint(3, 8), np.random.randint(3, 8)
    colors = [Color.RED, Color.BLUE, Color.GREEN]
    input_grid = np.zeros((n, m), dtype=int)
    
    for i in range(n):
        for j in range(m):
            if np.random.rand() > 0.7:
                input_grid[i, j] = np.random.choice(colors)
    
    return input_grid
    
# Example of usage:
# input_grid = generate_input()
# output_grid = main(input_grid)