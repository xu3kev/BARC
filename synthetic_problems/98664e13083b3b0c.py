from common import *
import numpy as np
from typing import *

# concepts:
# diagonals, color presence, flood fill

# description:
# In the input, you will see a grid with colored pixels forming multiple diagonal lines intersecting at some points.
# To make the output, find all the diagonals, and if a colorful pixel is present at any of the intersection points, flood fill the whole diagonal with the color of that pixel intersecting.
# If multiple diagonals have intersecting pixels of different colors, leave the intersection point unchanged.

def main(input_grid):
    # Create an output grid initialized as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Identify the dimensions of the input grid
    rows, cols = input_grid.shape

    # Function to get the diagonals
    def get_diagonals(grid, direction='both'):
        diagonals = []
        for i in range(rows + cols - 1):
            if direction == 'both' or direction == 'main':
                diag_main = [grid[i - j, j] for j in range(max(0, i - rows + 1), min(i + 1, cols))]
                diagonals.append(diag_main)
                
            if direction == 'both' or direction == 'anti':
                diag_anti = [grid[j, i - j] for j in range(max(0, i - cols + 1), min(i + 1, rows))]
                diagonals.append(diag_anti)
        return diagonals

    # Get both sets of diagonals
    diagonals_main = get_diagonals(input_grid, direction='main')
    diagonals_anti = get_diagonals(input_grid, direction='anti')

    # Process each diagonal for flood fill
    for diag in diagonals_main + diagonals_anti:
        color_presence = {}
        for idx, color in enumerate(diag):
            if color != Color.BLACK:
                color_presence[color] = color_presence.get(color, []) + [idx]

        for color, indices in color_presence.items():
            for idx in indices:
                flood_fill(output_grid, idx, idx, color, connectivity=4)

    return output_grid

def generate_input():
    rows, cols = 10, 10
    grid = np.full((rows, cols), Color.BLACK)

    # Randomly choose number of diagonals and their colors
    num_diagonals = np.random.randint(2, min(rows, cols)-1)
    colors = random.choices(list(Color.NOT_BLACK), k=num_diagonals)

    for i in range(num_diagonals):
        color = colors[i]
        diag_type = np.random.choice(['main', 'anti'])
        
        # Random starting point based on diagonal type
        if diag_type == 'main':
            start_row = np.random.randint(0, rows - 3)
            start_col = np.random.randint(0, cols - 3)
            for j in range(min(rows - start_row, cols - start_col)):
                grid[start_row + j, start_col + j] = color
        else:
            start_row = np.random.randint(0, rows - 3)
            start_col = np.random.randint(3, cols)
            for j in range(min(start_row + 1, start_col + 1)):
                grid[start_row - j, start_col - j] = color

    return grid