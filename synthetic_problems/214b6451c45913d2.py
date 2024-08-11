from common import *

import numpy as np
from typing import *

# concepts:
# lines, color, pixel manipulation

# description:
# In the input you will see a green pixel and a red pixel.
# To make the output, draw a diagonal blue line from the green pixel to the red pixel, and then duplicate the vertical differences in each column along the diagonal.

def main(input_grid: np.ndarray) -> np.ndarray:
    # copy the input grid to the output grid
    output_grid = np.copy(input_grid)
    
    # find the green and red pixels
    green_x, green_y = np.where(input_grid == Color.GREEN)
    red_x, red_y = np.where(input_grid == Color.RED)
    
    green_x, green_y = green_x[0], green_y[0]
    red_x, red_y = red_x[0], red_y[0]
    
    # Calculate the differences
    dx = np.sign(red_x - green_x)
    dy = np.sign(red_y - green_y)
    
    x, y = green_x, green_y
    
    # Draw the diagonal blue line
    while (x != red_x) and (y != red_y):
        if 0 <= x < input_grid.shape[0] and 0 <= y < input_grid.shape[1]:
            output_grid[x, y] = Color.BLUE
            
        x += dx
        y += dy
    
    # Draw the red pixel to the new location
    if 0 <= red_x < input_grid.shape[0] and 0 <= red_y < input_grid.shape[1]:
        output_grid[red_x, red_y] = Color.RED
    
    return output_grid

def generate_input() -> np.ndarray:
    # make a black grid as the background
    n = np.random.randint(10, 20)
    m = np.random.randint(10, 20)
    grid = np.zeros((n, m), dtype=int)
    
    # select a random position for the green pixel
    green_x = np.random.randint(0, n)
    green_y = np.random.randint(0, m)
    grid[green_x, green_y] = Color.GREEN
    
    # select a random position for the red pixel
    red_x = np.random.randint(0, n)
    red_y = np.random.randint(0, m)
    grid[red_x, red_y] = Color.RED
    
    # check if the green and red pixels are in the same row, column, or diagonal
    # if they are, then try again
    if green_x == red_x or green_y == red_y or abs(green_x - red_x) != abs(green_y - red_y):
        return generate_input()
    
    return grid