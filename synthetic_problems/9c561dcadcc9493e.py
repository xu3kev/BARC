from common import *
import numpy as np
from typing import *

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Find all non-black colored pixels in the grid
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    
    for x, y in colored_pixels:
        color = input_grid[x, y]
        # Extend diagonals in both directions
        direction1 = (1, 1) if (x + y) % 2 == 0 else (-1, -1)
        direction2 = (-1, -1) if (x + y) % 2 == 0 else (1, 1)

        draw_line(output_grid, x, y, length=None, color=color, direction=direction1, stop_at_color=Color.NOT_BLACK)
        draw_line(output_grid, x, y, length=None, color=color, direction=direction2, stop_at_color=Color.NOT_BLACK)
    
    # Apply diagonal mirror symmetry for all the set pixels
    for x in range(output_grid.shape[0]):
        for y in range(output_grid.shape[1]):
            if output_grid[x, y] != Color.BLACK:
                mirrored_x, mirrored_y = y, x
                output_grid[mirrored_x, mirrored_y] = output_grid[x, y]
    
    return output_grid

def generate_input():
    grid = np.full((10, 10), Color.BLACK)
    colors = np.random.choice(list(Color.NOT_BLACK), 3, replace=False)
    
    # Create three diagonal lines with different starting edges and colors
    for color in colors:
        start_edge = np.random.choice(['left', 'top', 'right', 'bottom'])
        if start_edge == 'left':
            start_x, start_y = np.random.randint(0, 10), 0
        elif start_edge == 'top':
            start_x, start_y = 0, np.random.randint(0, 10)
        elif start_edge == 'right':
            start_x, start_y = np.random.randint(0, 10), 9
        else:  # bottom
            start_x, start_y = 9, np.random.randint(0, 10)
        
        draw_diagonal(grid, start_x, start_y, color)
    
    return grid

def draw_diagonal(grid, x, y, color):
    # create diagonal line
    if (x + y) % 2 == 0:
        draw_line(grid, x, y, length=None, color=color, direction=(1, 1), stop_at_color=Color.NOT_BLACK)
    else:
        draw_line(grid, x, y, length=None, color=color, direction=(-1, -1), stop_at_color=Color.NOT_BLACK)