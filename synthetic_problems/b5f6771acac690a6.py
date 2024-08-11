from common import *

import numpy as np
import random

# concepts:
# symmetries, colors

# description:
# In the input grid, you will see various colored pixels arranged in a grid. Each color should be paired with another randomly chosen color. The output grid will have each pair of colors swapped.
# For example, blue might be paired with red and green might be paired with yellow. So wherever there was blue, it is now red and vice versa. Wherever there was green, it is now yellow and vice versa.

def main(input_grid):
    output_grid = np.copy(input_grid)
    
    # Define the pairs of colors to swap
    color_pairs = [(Color.BLUE, Color.RED), (Color.GREEN, Color.YELLOW), (Color.TEAL, Color.ORANGE), (Color.PINK, Color.MAROON)]
    
    # Perform the swaps for each pair
    for color1, color2 in color_pairs:
        temp_mask = input_grid == color1
        output_grid[input_grid == color2] = color1
        output_grid[temp_mask] = color2

    return output_grid

def generate_input():
    n = random.randint(10, 20)
    m = random.randint(10, 20)
    grid = np.empty((n, m), dtype=object)
    
    # Select the colors to use
    color_palette = [Color.BLUE, Color.RED, Color.GREEN, Color.YELLOW, Color.TEAL, Color.ORANGE, Color.PINK, Color.MAROON]
    color_pairs = [(Color.BLUE, Color.RED), (Color.GREEN, Color.YELLOW), (Color.TEAL, Color.ORANGE), (Color.PINK, Color.MAROON)]

    # Populate the grid randomly with the colors from the color palette
    for i in range(n):
        for j in range(m):
            grid[i, j] = random.choice(color_palette)
    
    return grid