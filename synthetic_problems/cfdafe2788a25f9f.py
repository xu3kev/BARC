from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, repetition, coloring diagonal pixels

# description:
# Given an input grid with a pattern encapsulated by horizontal symmetrical borders, create an output grid by first mirroring the pattern horizontally and then copying it below.
# Lastly, color all the diagonal adjacent black pixels teal.

def main(input_grid):
    # Find the pattern by removing top and bottom symmetric borders
    t, b = detect_border_indices(input_grid)
    pattern = input_grid[t+1:b, :]
    
    # Mirror the pattern horizontally
    mirrored_pattern = np.flip(pattern, axis=1)

    # Combine the original and mirrored pattern
    combined_pattern = np.concatenate((pattern, mirrored_pattern), axis=0)
    
    # Replicate the combined pattern below the original
    output_grid = np.concatenate((combined_pattern, combined_pattern), axis=0)
    
    # Color diagonal pixels
    diagonal_dx_dy = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    for y in range(output_grid.shape[1]):
        for x in range(output_grid.shape[0]):
            if output_grid[x, y] != Color.BLACK and output_grid[x, y] != Color.TEAL:
                for dx, dy in diagonal_dx_dy:
                    if 0 <= x + dx < output_grid.shape[0] and 0 <= y + dy < output_grid.shape[1] and output_grid[x + dx, y + dy] == Color.BLACK:
                        output_grid[x + dx, y + dy] = Color.TEAL
                        
    return output_grid


def generate_input():
    # Choose random size for pattern and vertical padding
    n, m = np.random.randint(5, 10), np.random.randint(5, 10)
    padding = np.random.randint(1, 3)
    
    # Create the basic empty pattern grid
    pattern = random_sprite(n, m, density=0.5, color_palette=list(Color.NOT_BLACK), connectivity=4)
    
    # Add horizontal symmetric borders
    symmetric_border = np.random.choice(Color.NOT_BLACK)
    grid = np.pad(pattern, ((padding, padding), (0, 0)), mode='constant', constant_values=Color.BLACK)
    
    # Set symmetric borders color
    grid[:padding, :] = symmetric_border
    grid[-padding:, :] = symmetric_border
    
    return grid


def detect_border_indices(input_grid, background=Color.BLACK):
    # Detect the indices of the top and bottom symmetric borders
    symmetric_border_color = None
    t, b = 0, input_grid.shape[0] - 1

    for i in range(input_grid.shape[0]):
        if np.all(input_grid[i] != background):
            symmetric_border_color = input_grid[i][0]
            t = i
            break
    
    for i in range(input_grid.shape[0] - 1, -1, -1):
        if np.all(input_grid[i] == symmetric_border_color):
            b = i
            break

    return t, b