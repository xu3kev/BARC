from common import *

import numpy as np
from typing import *

# concepts:
# patterns, lines, pixel manipulation

# description:
# In the input, you will see a grid with a top row consisting of a sequence of colored pixels, with each color representing a pattern.
# To make the output, copy the first row of the input to the output.
# Then, starting from the second row onwards, draw diagonal lines starting from each pixel in the first row.
# The color of each diagonal line will match the color of the corresponding pixel in the first row.
# Each diagonal line will slope downwards to the right.

def main(input_grid):
    # create an output grid initialized with the input grid
    output_grid = np.copy(input_grid)
    
    # get the colors from the top row
    colors = input_grid[:, 0]
    
    # draw the diagonal lines for each color in the top row
    for col in range(len(colors)):
        for row in range(1, input_grid.shape[1]):
            x = col
            y = row
            if x < input_grid.shape[0] and y < input_grid.shape[1]:
                output_grid[x, y] = colors[col]
                col += 1
    
    return output_grid

def generate_input():
    # random grid height (rows count more than colors count)
    n = np.random.randint(5, 10)
    # number of colors in the top row
    num_colors = np.random.randint(3, 7)
    
    # creating a grid with initial background color
    grid = np.zeros((num_colors, n), dtype=int)
    
    # fill the top row with random colors
    colors = np.random.choice(list(Color.NOT_BLACK), num_colors, replace=False)
    for i in range(num_colors):
        grid[i, 0] = colors[i]
    
    return grid