from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines, repetition

# description:
# In the input you will see a 7x7 grid, with three diagonal lines that stretch from one end of the canvas to the other
# Each line is a different color, and the colors are not black
# The output should be the result of repeating every diagonal line on multiples of 3 offset from the original, which gives an interlacing pattern filling the output canvas


def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.zeros((7, 7), dtype=int)

    # Loop over the input looking for any of the three diagonals
    # If we find one, we will fill the output with the same color in the same pattern
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            c = input_grid[i][j]
            if c != Color.BLACK:
                # Fill the output with the same color in the same pattern
                # Loop by multiples of 3 to create the pattern
                # Loop way beyond the canvas (double the canvas size) to make sure we cover everything
                for distance in range(0, output_grid.shape[0]*2, 3):
                    draw_diagonal(output_grid, i-distance, j, c)
                    draw_diagonal(output_grid, i+distance, j, c)
    
    return output_grid

def draw_diagonal(grid, x, y, c):
    # create diagonal line that stretches from one side of the canvas to the other
    # to do this, draw infinite rays pointing in opposite directions
    draw_line(grid, x, y, length=None, color=c, direction=(1, -1))
    draw_line(grid, x, y, length=None, color=c, direction=(-1, 1))

def generate_input() -> np.ndarray:

    # create a 7x7 grid of black (0)
    grid = np.zeros((7, 7), dtype=int)
    # pick 3 random distinct colors
    c1, c2, c3 = np.random.choice(Color.NOT_BLACK, 3, replace=False)

    # put down the three diagonal lines
    draw_diagonal(grid, np.random.choice(range(7)), np.random.choice(range(7)), c1)
    draw_diagonal(grid, np.random.choice(range(7)), np.random.choice(range(7)), c2)
    draw_diagonal(grid, np.random.choice(range(7)), np.random.choice(range(7)), c3)

    # make sure that the output is completely filled up with the pattern meaning it doesn't contain any black pixels
    if np.any(main(grid) == Color.BLACK):
        return generate_input()
    
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)