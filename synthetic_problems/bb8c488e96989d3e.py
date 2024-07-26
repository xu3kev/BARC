from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, alignment, colors as indicators

# description:
# In the input, you will see a grid with monochromatic squares (each of one unit length) of three different colors placed randomly. 
# To make the output, group all the squares by color and place them vertically aligned in separate columns in the output grid.

def main(input_grid):
    # Determine the non-black colors in the grid
    colors = [Color.RED, Color.BLUE, Color.YELLOW]

    # Prepare an empty list to collect grouped squares by color
    grouped_squares = {color: [] for color in colors}
    
    # Gather the coordinates of each color square
    for color in colors:
        coords = np.argwhere(input_grid == color)
        grouped_squares[color] = coords
    
    # Calculate the dimensions of the output grid
    output_grid_height = max(len(grouped_squares[Color.RED]), len(grouped_squares[Color.BLUE]), len(grouped_squares[Color.YELLOW]))
    output_grid_width = 3  # Three columns for three different colors
    
    # Create the output grid filled with black color
    output_grid = np.full((output_grid_height, output_grid_width), Color.BLACK, dtype=int)
    
    # Place squares in columns based on their color
    for col, color in enumerate(colors):
        for row, (x, y) in enumerate(grouped_squares[color]):
            output_grid[row, col] = color

    return output_grid

def generate_input():
    # Create a random grid size
    n = np.random.randint(6, 10)
    m = np.random.randint(6, 10)
    grid = np.full((n, m), Color.BLACK, dtype=int)
    
    colors = [Color.RED, Color.BLUE, Color.YELLOW]
    
    # Place 5-10 randomly colored squares in the grid
    for i in range(np.random.randint(5, 11)):
        x = np.random.randint(0, n)
        y = np.random.randint(0, m)
        color = np.random.choice(colors)
        grid[x, y] = color
    
    return grid