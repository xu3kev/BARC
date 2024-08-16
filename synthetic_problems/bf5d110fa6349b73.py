from common import *

import numpy as np
from typing import *

# concepts:
# connecting same color, filling, pixel manipulation

# description:
# In the input, each pixel inside the grid is either completely shaped like a symbol '+' or surrounded by random placement of colored pixels.
# To make the output, each '+' shaped symbol's color get spread out in horizontal and vertical direction filling all the way to the boundary of the grid until it meets another shape or edge.

def main(input_grid):
    output_grid = np.copy(input_grid)

    # find the '+' symbols in the grid
    n, m = input_grid.shape
    for i in range(1, n-1):
        for j in range(1, m-1):
            if input_grid[i, j] != Color.BLACK:
                center_color = input_grid[i, j]
                
                if (input_grid[i-1, j] == center_color and 
                    input_grid[i+1, j] == center_color and
                    input_grid[i, j-1] == center_color and
                    input_grid[i, j+1] == center_color):
                    
                    # fill horizontally left
                    for x in range(j-1, -1, -1):
                        if input_grid[i, x] != Color.BLACK and input_grid[i, x] != center_color:
                            break
                        output_grid[i, x] = center_color
                    
                    # fill horizontally right
                    for x in range(j+1, m):
                        if input_grid[i, x] != Color.BLACK and input_grid[i, x] != center_color:
                            break
                        output_grid[i, x] = center_color
                    
                    # fill vertically up
                    for y in range(i-1, -1, -1):
                        if input_grid[y, j] != Color.BLACK and input_grid[y, j] != center_color:
                            break
                        output_grid[y, j] = center_color
                    
                    # fill vertically down
                    for y in range(i+1, n):
                        if input_grid[y, j] != Color.BLACK and input_grid[y, j] != center_color:
                            break
                        output_grid[y, j] = center_color

    return output_grid

def generate_input():
    n, m = np.random.randint(8, 15), np.random.randint(8, 15)
    grid = np.full((n, m), Color.BLACK, dtype=int)
    
    num_plus_symbols = np.random.randint(2, 5)
    
    for _ in range(num_plus_symbols):
        color = random.choice(list(Color.NOT_BLACK))
        
        # randomly select center for the '+' symbol
        i, j = np.random.randint(1, n-1), np.random.randint(1, m-1)
        
        # if the location is not suitable, try again
        if ((grid[i, j] != Color.BLACK) or
            (grid[i-1, j] != Color.BLACK) or
            (grid[i+1, j] != Color.BLACK) or
            (grid[i, j-1] != Color.BLACK) or
            (grid[i, j+1] != Color.BLACK)):
            continue
        
        # create the '+' symbol
        grid[i, j] = color
        grid[i-1, j] = color
        grid[i+1, j] = color
        grid[i, j-1] = color
        grid[i, j+1] = color
        
        # randomly place some other colored pixels
        num_random_pixels = np.random.randint(1, 4)
        for _ in range(num_random_pixels):
            ri, rj = np.random.randint(0, n), np.random.randint(0, m)
            grid[ri, rj] = random.choice(list(Color.NOT_BLACK))
    
    return grid