from common import *

import numpy as np
from typing import *

# concepts:
# symmetry detection, repetition, coloring diagonal pixels

# description:
# Given an input grid containing colored shapes with diagonal symmetry but partially covered by black pixels, the task is to restore the symmetry for each shape.
# Then replicate the entire grid three times horizontally. Finally, any black pixel adjacent to a colored pixel in the output grid should be colored teal.

def main(input_grid):
    # Restore the symmetry of each shape
    output_grid = input_grid.copy()
    sym = detect_rotational_symmetry(input_grid, ignore_colors=[Color.BLACK])
    
    for x, y in np.argwhere(input_grid != Color.BLACK):
        color = input_grid[x, y]
        for i in range(1, 4):
            rotated_x, rotated_y = sym.apply(x, y, iters=i)
            if output_grid[rotated_x, rotated_y] == Color.BLACK:
                output_grid[rotated_x, rotated_y] = color

    # Initialize horizontally repeated grid
    h_rep_grid = np.zeros((output_grid.shape[0], 3 * output_grid.shape[1]), dtype=int)

    for i in range(3):
        blit_sprite(h_rep_grid, output_grid, 0, i * output_grid.shape[1])

    # Color black pixels adjacent to colored pixels as Teal
    diagonal_dx_dy = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    
    for y in range(h_rep_grid.shape[1]):
        for x in range(h_rep_grid.shape[0]):
            if h_rep_grid[x, y] != Color.BLACK and h_rep_grid[x, y] != Color.TEAL:
                for dx, dy in diagonal_dx_dy:
                    if (0 <= x + dx < h_rep_grid.shape[0] and 
                        0 <= y + dy < h_rep_grid.shape[1] and 
                        h_rep_grid[x + dx, y + dy] == Color.BLACK):
                        h_rep_grid[x + dx, y + dy] = Color.TEAL

    return h_rep_grid


def generate_input():
    n, m = np.random.randint(5, 7), np.random.randint(5, 7)
    grid = np.zeros((n, m), dtype=int)
    
    # Create diagonally symmetric sprite
    sprite = random_sprite(3, 3, density=0.5, symmetry="diagonal", color_palette=list(Color.NOT_BLACK))
    
    # Randomly remove pixels to create partial occlusion
    for i in range(sprite.shape[0]):
        for j in range(sprite.shape[1]):
            if np.random.random() < 0.2:
                sprite[i, j] = Color.BLACK

    # Place sprites randomly on the grid
    x, y = random_free_location_for_sprite(grid, sprite)
    blit_sprite(grid, sprite, x, y)

    return grid