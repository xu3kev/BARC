from common import *

import numpy as np
from typing import *

# concepts:
# diagonal lines

# description:
# In the input you will see one colored pixel on a black background.
# To make the output, make two diagonal lines that are the same color as the colored pixel and intersect at the location of the colored pixel.

def main(input_grid):
    # make output grid
    output_grid = np.copy(input_grid)

    # get the index of the colored pixel
    x, y, width, height = bounding_box(input_grid != Color.BLACK)
    
    # get color from colored pixel
    color = input_grid[x,y]

    # draw diagonals
    # first diagonal
    draw_line(output_grid, x, y, length=None, color=color, direction=(1, -1))
    draw_line(output_grid, x, y, length=None, color=color, direction=(-1, 1))
    # second diagonal
    draw_line(output_grid, x, y, length=None, color=color, direction=(-1, -1))
    draw_line(output_grid, x, y, length=None, color=color, direction=(1, 1))

    return output_grid

    



def generate_input():
    # make a square black grid for the background first
    n = m = np.random.randint(5, 20)
    grid = np.zeros((n, m), dtype=int)

    # put a randomly colored pixel at a random point on the grid
    color = random.choice(list(Color.NOT_BLACK))
    x, y = np.random.randint(0, n-1), np.random.randint(0, m-1)
    grid[x,y] = color

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)