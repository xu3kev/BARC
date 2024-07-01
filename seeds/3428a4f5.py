from common import *

import numpy as np
from typing import *

# concepts:
# bitmasks with separator, boolean logical operations

# description:
# Compute the XOR operation of where the two grids are red, turning the output green in those locations.
# In the input, you should see two 6x5 red patterns on top and bottom separated a horizontal yellow line in the middle of the grid.
# To make the output, you have to overlap the two patterns. If the overlapping cells are the same color, then the corresponding cell is colored black; otherwise, 
# if the overlapping cells are not the same color, then the corresponding cell is colored green

def main(input_grid):

    width, height = input_grid.shape
   
    # Find the yellow horizontal line/bar
    for y_bar in range(height):
        if np.all(input_grid[:, y_bar] == Color.YELLOW):
            break
    
    # extract left and right patterns
    left_pattern = input_grid[:, :y_bar]
    right_pattern = input_grid[:, y_bar+1:] 

    output_grid = np.zeros_like(left_pattern)

    # applying the XOR pattern, which is where they are different
    output_grid[(left_pattern!=right_pattern)] = Color.GREEN
    output_grid[(left_pattern==right_pattern)] = Color.BLACK

    return output_grid


def generate_input():
  
    # Define the grid size
    width = 5  
    height = 13 # 6 top + 1 yellow line + 6 bottom

    # Initialize an empty grid
    input_grid = np.full((width, height), Color.BLACK)

    # Randomly assign red or black to the top and bottom patterns
    for x in range(width):
        for y in range(height):
            input_grid[x, y] = np.random.choice([Color.BLACK, Color.RED])

    # Set the yellow vertical line
    input_grid[:, int(height//2)] = Color.YELLOW

    return input_grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)