from common import *

import numpy as np
from typing import *

# concepts:
# line detection, color extraction

# description:
# In the input you will see a grid with several horizontal or vertical lines of different colors.
# To make the output, make a grid with one horizontal line or vertical line for each color, 
# in the order they appear in the input.

def main(input_grid):
    # Determine whether the lines are horizontal or vertical
    symmetry = detect_mirror_symmetry(grid=input_grid)[0]
    if symmetry.mirror_x is None:
        if_horizontal = False
    else:
        if_horizontal = True
    
    # If the lines are horizontal, rotate the grid to make them vertical for easier processing
    if if_horizontal:
        input_grid = np.rot90(input_grid, k=3)
    n, m = input_grid.shape

    # Extract the colors of the lines
    # One line may have different width
    color_list = []
    for i in range(n):
        if i == 0:
            color_list.append(input_grid[i][0])
        elif input_grid[i][0] != color_list[-1]:
            color_list.append(input_grid[i][0])
    # Generate the output grid, one horizontal line for each color
    output_grid = np.array([color_list])

    # If the lines are vertical, transpose the output grid to make it vertical
    if not if_horizontal:
        output_grid = np.transpose(output_grid)
    
    # Return the output grid
    return output_grid

def generate_input():
    # Generate grid of size n x m, ensure n > m
    n, m = np.random.randint(3, 10), np.random.randint(1, 10)
    if n < m:
        n, m = m, n
    grid = np.zeros((n, m), dtype=int)

    # Randomly choose n colors
    colors = np.random.choice(list(Color.NOT_BLACK), n)
    
    # Draw vertical lines of the chosen colors
    for i, color in enumerate(colors):
        draw_line(grid=grid, x=i, y=0, length=m, color=color, direction=(0, 1))
    # Randomly rotate the whole grid to make the lines horizontal or vertical
    if_rotate = np.random.choice([True, False])
    if if_rotate:
        grid = np.rot90(grid)

    return grid



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
