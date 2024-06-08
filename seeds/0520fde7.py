import numpy as np
from typing import *
from common import *

# concepts:
# boolean logical operations, bitmasks with separator

# description:
# Compute the AND of where two 3x3 grids are both blue, turning the output red in those locations
# The input grids are separated by a gray divider column in the middle
# The output grid is a 3x3 grid

def main(input_grid: np.ndarray) -> np.ndarray:
    # Extract the left and right 3x3 grids from the input
    left_input = input_grid[:3, :]
    right_input = input_grid[4:7, :]

    # Create an output grid
    output_grid = np.zeros((3,3), dtype=int)
    for i in range(3):
        for j in range(3):
            # If both the left and right grids are blue, set the output to red
            if left_input[i][j] == Color.BLUE and right_input[i][j] == Color.BLUE:
                output_grid[i][j] = Color.RED

    return output_grid

# make 2 3x3 grid of black and blue, and put them side by side with a gray 3x1 division in the middle
def generate_input() -> np.ndarray:
    # create a 3x3 grid of black (0)
    grid1 = np.zeros((3, 3), dtype=int)
    # sparsely populate it with blue
    for x in range(3):
        for y in range(3):
            if np.random.random() < 0.5:
                grid1[x,y] = Color.BLUE

    # create a 3x3 grid of black (0)
    grid2 = np.zeros((3, 3), dtype=int)
    # sparsely populate it with blue
    for x in range(3):
        for y in range(3):
            if np.random.random() < 0.3:
                grid2[x,y] = Color.BLUE
    
    # create a 1x3 grid of gray (the divider)
    grid3 = np.zeros((1, 3), dtype=int)
    grid3[0, :] = Color.GRAY

    # concatenate the three grids
    grid = np.concatenate((grid1, grid3, grid2), axis=0)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
